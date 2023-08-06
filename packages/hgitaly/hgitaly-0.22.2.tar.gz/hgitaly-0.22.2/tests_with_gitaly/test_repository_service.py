# Copyright 2021 Sushil Khanchi <sushilkhanchi97@gmail.com>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
from mercurial import (
    node as node_mod,
    pycompat,
)
import pytest
import grpc
import itertools
# from hgitaly.git import EMPTY_TREE_OID
from hgitaly.stub.shared_pb2 import Repository
from hgitaly.stub.repository_service_pb2 import (
    CreateRepositoryRequest,
    FindMergeBaseRequest,
    SetFullPathRequest,
)
from hgitaly.stub.repository_service_pb2_grpc import RepositoryServiceStub

from . import skip_comparison_tests
if skip_comparison_tests():  # pragma no cover
    pytestmark = pytest.mark.skip


def test_compare_find_merge_base(gitaly_comparison):
    fixture = gitaly_comparison
    gitaly_repo = fixture.gitaly_repo
    git_repo = fixture.git_repo
    wrapper = fixture.hg_repo_wrapper

    # repo structure:
    #
    #   o 3 add animal (branch/stable)
    #   |
    #   | 2 add bar
    #   |/
    #   o 1 add zoo
    #   |
    #   o 0 add foo
    #
    gl_branch = b'branch/default'
    sha0 = wrapper.write_commit('foo').hex()
    git_shas = {
        sha0: git_repo.branches()[gl_branch]['sha']
    }
    ctx1 = wrapper.write_commit('zoo')
    sha1 = ctx1.hex()
    git_shas[sha1] = git_repo.branches()[gl_branch]['sha']
    sha2 = wrapper.write_commit('bar').hex()
    git_shas[sha2] = git_repo.branches()[gl_branch]['sha']
    sha3 = wrapper.write_commit('animal', branch='stable', parent=ctx1).hex()
    git_shas[sha3] = git_repo.branches()[b'branch/stable']['sha']
    # commiting a new root, which will test the case when there
    # is no merge_base (gca)
    sha4 = wrapper.commit_file('tut', branch='other',
                               parent=node_mod.nullid).hex()
    git_shas[sha4] = git_repo.branches()[b'branch/other']['sha']

    diff_stubs = dict(
        git=RepositoryServiceStub(fixture.gitaly_channel),
        hg=RepositoryServiceStub(fixture.hgitaly_channel),
    )

    def do_rpc(vcs, revisions):
        if vcs == 'git':
            revs = [git_shas.get(rev, rev) for rev in revisions]
            revisions = revs

        request = FindMergeBaseRequest(
            repository=gitaly_repo,
            revisions=revisions,
        )

        response = diff_stubs[vcs].FindMergeBase(request)
        base = pycompat.sysbytes(response.base)
        if not base:
            return base
        return base if vcs == 'git' else git_shas[base]

    list_of_interesting_revs = [b'branch/default', b'branch/stable',
                                sha0, sha1, sha4]
    for rev_pair in itertools.product(list_of_interesting_revs, repeat=2):
        assert do_rpc('hg', rev_pair) == do_rpc('git', rev_pair)

    # test with invalid_argument, as it requires minimum 2 revisions
    with pytest.raises(grpc.RpcError) as exc_info_hg:
        do_rpc('hg', [sha0])
    with pytest.raises(grpc.RpcError) as exc_info_git:
        do_rpc('git', [git_shas[sha0]])
    assert exc_info_hg.value.code() == exc_info_git.value.code()
    assert exc_info_hg.value.details() == exc_info_git.value.details()

    sha_not_exists = b'deadnode' * 5
    assert (
        do_rpc('hg', [sha0, sha_not_exists])
        ==
        do_rpc('git', [git_shas[sha0], sha_not_exists])
    )


def test_create_repository(gitaly_channel, grpc_channel, server_repos_root):
    rel_path = 'sample_repo'
    default_storage = 'default'
    repo_stubs = dict(
        hg=RepositoryServiceStub(grpc_channel),
        git=RepositoryServiceStub(gitaly_channel)
    )

    def do_rpc(vcs, rel_path, storage=default_storage):
        grpc_repo = Repository(relative_path=rel_path,
                               storage_name=storage)
        request = CreateRepositoryRequest(repository=grpc_repo)
        response = repo_stubs[vcs].CreateRepository(request)
        return response

    hg_rel_path = rel_path + '.hg'
    git_rel_path = rel_path + '.git'
    # actual test
    assert do_rpc('hg', hg_rel_path) == do_rpc('git', git_rel_path)

    # when repo already exists (actually its directory)
    with pytest.raises(grpc.RpcError) as exc_info_git:
        do_rpc('git', git_rel_path)
    with pytest.raises(grpc.RpcError) as exc_info_hg:
        do_rpc('hg', hg_rel_path)
    assert exc_info_hg.value.code() == exc_info_git.value.code()

    # when storage name is invalid
    with pytest.raises(grpc.RpcError) as exc_info_hg:
        do_rpc('hg', rel_path, storage='cargoship')
    with pytest.raises(grpc.RpcError) as exc_info_git:
        do_rpc('git', rel_path, storage='cargoship')
    assert exc_info_hg.value.code() == exc_info_git.value.code()
    assert 'no such storage' in exc_info_hg.value.details()
    assert 'no such storage' in exc_info_git.value.details()

    # test with a broken symlink (which points to itself)
    # it used to be an error for both, with Gitaly complaining
    # that the file exists (but would not raise an error for
    # an existing proper Git repo). As of 14.6, Gitaly refuses
    # all existing files, including broken symlinks
    # As a consequence of the added early check, we don't have
    # any case of `hg init` itself failing on hand.
    repo_name = "myrepo_a_broken_symlink"
    path = (server_repos_root / default_storage / repo_name)
    path.symlink_to(path)
    with pytest.raises(grpc.RpcError) as exc_info_hg:
        do_rpc('hg', repo_name)
    with pytest.raises(grpc.RpcError) as exc_info_git:
        do_rpc('git', repo_name)
    exc_hg, exc_git = exc_info_hg.value, exc_info_git.value
    assert exc_hg.code() == exc_git.code()
    for exc in (exc_hg, exc_git):
        assert 'exists already' in exc.details()


def test_set_full_path(gitaly_comparison, server_repos_root):
    fixture = gitaly_comparison

    repo_stubs = dict(
        hg=RepositoryServiceStub(fixture.hgitaly_channel),
        git=RepositoryServiceStub(fixture.gitaly_channel)
    )

    def do_rpc(vcs, path, grpc_repo=fixture.gitaly_repo):
        return repo_stubs[vcs].SetFullPath(
            SetFullPathRequest(repository=grpc_repo, path=path))

    def assert_compare(path):
        assert do_rpc('hg', path) == do_rpc('git', path)

    def assert_error_compare(path,
                             grpc_repo=None,
                             msg_normalizer=lambda m: m):
        kwargs = dict(grpc_repo=grpc_repo) if grpc_repo is not None else {}
        with pytest.raises(Exception) as hg_exc_info:
            do_rpc('hg', path, **kwargs)
        with pytest.raises(Exception) as git_exc_info:
            do_rpc('git', path, **kwargs)
        hg_exc, git_exc = hg_exc_info.value, git_exc_info.value
        assert hg_exc.code() == git_exc.code()
        hg_msg, git_msg = hg_exc.details(), git_exc.details()
        assert msg_normalizer(hg_msg) == msg_normalizer(git_msg)

    # success case
    assert_compare('group/project')

    # error cases
    assert_error_compare('')

    def normalize_repo_not_found(msg):
        return msg.replace('git repo', 'Mercurial repo')

    assert_error_compare('some/full/path',
                         grpc_repo=Repository(
                             storage_name=fixture.gitaly_repo.storage_name,
                             relative_path='no/such/repo'),
                         msg_normalizer=normalize_repo_not_found,
                         )

    assert_error_compare('some/full/path',
                         grpc_repo=Repository(
                             relative_path=fixture.gitaly_repo.relative_path,
                             storage_name='unknown'))
