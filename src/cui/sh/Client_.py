import subprocess
import shlex
import copy
from web.log.Log import Log

# shell実行クライアント
# http://takuya-1st.hatenablog.jp/entry/2014/08/23/022031
class Client:
    __popen_args = {
        'bufsize':-1, 'executable':None, 'stdin':subprocess.PIPE, 'stdout':subprocess.PIPE, 'stderr':subprocess.PIPE, 'preexec_fn':None, 'close_fds':True, 'shell':False, 'cwd':None, 'env':None, 'universal_newlines':False, 'startupinfo':None, 'creationflags':0, 'restore_signals':True, 'start_new_session':False, 'pass_fds':(), 'encoding':None, 'errors':None
    }

    # shellコマンドを文字列で渡すと、実行し、結果を表示し、結果のテキストを返す
    @classmethod
    def Run(cls, command, *args, **popen_args):
        a = copy.copy(cls.__popen_args)
        if isinstance(popen_args, dict) : a.update(popen_args)
        return Client.__run(command, a)
        """
        cmd = shlex.split(command) # 文字列をsh構文単位で分割する
        if '|' in cmd: a['shell'] = True # パイプがあったらshell=Trueで文字列入力する（Popen()だと面倒なので）
        if popen_args['shell']: p = subprocess.Popen(command, **a)
        else: p = subprocess.Popen(cmd, **a)
        stdout_data, stderr_data = p.communicate()
        stdout_utf8 = stdout_data.decode('utf-8').strip()
        stderr_utf8 = stderr_data.decode('utf-8').strip()
        if 0 < len(stderr_utf8):
            Log().Logger.error(stderr_utf8)
            raise Exception('エラーが発生しました。\nコマンド:\n{}\nエラー:\n{}'.format(command, stderr_utf8))
        return stdout_utf8
        """

    def __init__(self, *args, **popen_args):
        #cwd = self.__popen_args.path_dir_pj,
        #shell = True # Falseだとコマンドを配列で渡すことになる。パイプを使えない。
        #stdout=subprocess.PIPE, stderr=subprocess.PIPE

        # Popenデフォルト値
        # https://docs.python.jp/3/library/subprocess.html#subprocess.Popen
        self.__popen_args = copy.deepcopy(Client.__popen_args)
        if isinstance(args, dict) : self.__popen_args.update(popen_args)

    # shellコマンドを文字列で渡すと、実行し、結果を表示し、結果のテキストを返す
    def run(self, command, *args, **popen_args):
        a = copy.copy(self.__popen_args)
        if isinstance(popen_args, dict) : a.update(popen_args)
        return Client.__run(command, a)
        """
        cmd = shlex.split(command) # 文字列をsh構文単位で分割する
        if '|' in cmd: a['shell'] = True # パイプがあったらshell=Trueで文字列入力する（Popen()だと面倒なので）
        if args['shell']: p = subprocess.Popen(command, **a)
        else: p = subprocess.Popen(cmd, **a)
        stdout_data, stderr_data = p.communicate()
        stdout_utf8 = stdout_data.decode('utf-8').strip()
        stderr_utf8 = stderr_data.decode('utf-8').strip()
        if 0 < len(stderr_utf8):
            web.log.Log.Log().Logger.error(stderr_utf8)
            raise Exception('エラーが発生しました。\nコマンド:\n{}\nエラー:\n{}'.format(command, stderr_utf8))
        return stdout_utf8
        """

    @staticmethod
    def __run(command, a):
        Log().Logger.debug(command)
        print(a)

        cmd = shlex.split(command) # 文字列をsh構文単位で分割する
        if '|' in cmd: a['shell'] = True # パイプがあったらshell=Trueで文字列入力する（Popen()だと面倒なので）
        if a['shell']: p = subprocess.Popen(command, **a)
        else: p = subprocess.Popen(cmd, **a)
        stdout_data, stderr_data = p.communicate()
        stdout_utf8 = stdout_data.decode('utf-8').strip()
        stderr_utf8 = stderr_data.decode('utf-8').strip()
        if 0 < len(stderr_utf8):
            Log().Logger.error(stderr_utf8)
            raise Exception('エラーが発生しました。\nコマンド:\n{}\nエラー:\n{}'.format(command, stderr_utf8))
        if 0 < len(stdout_utf8):
            Log().Logger.info(stdout_utf8)
        
        return stdout_utf8
        
