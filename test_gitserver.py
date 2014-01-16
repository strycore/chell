import os
import pwd
import unittest

GIT_REPO_ROOT = "/srv/git"
GIT_USER = 'git'


class TestGitServer(unittest.TestCase):
    def test_repo_exists(self):
        self.assertTrue(os.path.isdir(GIT_REPO_ROOT))

    def test_git_user_is_correctly_configured(self):
        user = pwd.getpwnam(GIT_USER)
        self.assertEqual(user.pw_dir, GIT_REPO_ROOT)
        self.assertEqual(user.pw_shell, '/usr/bin/git-shell')

    def test_repo_has_correct_owner(self):
        repo_stat = os.stat(GIT_REPO_ROOT)
        repo_uid = repo_stat.st_uid
        user = pwd.getpwuid(repo_uid)
        self.assertEqual(user.pw_name, GIT_USER)

    def test_git_repo_has_ssh_configured(self):
        ssh_dir = os.path.join(GIT_REPO_ROOT, ".ssh")
        self.assertTrue(os.path.exists(ssh_dir))

        git_user = pwd.getpwnam(GIT_USER)
        ssh_stat = os.stat(ssh_dir)
        self.assertEqual(ssh_stat.st_uid, git_user.pw_uid)
        self.assertEqual(ssh_stat.st_gid, git_user.pw_gid)

        keys_file = os.path.join(ssh_dir, 'authorized_keys')
        self.assertTrue(os.path.exists(keys_file))
        keys_stat = os.stat(keys_file)
        self.assertEqual(keys_stat.st_uid, git_user.pw_uid)
        self.assertEqual(keys_stat.st_gid, git_user.pw_gid)

    def test_git_repo_has_create_command(self):
        commands_dir = os.path.join(GIT_REPO_ROOT, 'git-shell-commands')
        self.assertTrue(os.path.exists(commands_dir))

        create_command = os.path.join(commands_dir, 'create')
        self.assertTrue(os.path.exists(create_command))

if __name__ == '__main__':
    unittest.main()
