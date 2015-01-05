import gflags
import os

FLAGS = gflags.FLAGS

gflags.DEFINE_string("src",  None, "source directory")
gflags.DEFINE_string("dest", None, "destination directory")
gflags.DEFINE_bool("dryrun", False, "dryrun")
gflags.DEFINE_enum("cmd", None, ["link", "symlink"], "command")
gflags.MarkFlagAsRequired("src")
gflags.MarkFlagAsRequired("dest")
gflags.MarkFlagAsRequired("cmd")


class _Funcs(object):

    def __init__(self):
        self._dest_funcs = dict()
        self._name_funcs = []

        def _filename(root, filename):
            return filename
        self._name_funcs.append(_filename)

        self._commands = dict(
            link=os.link,
            symlink=os.symlink
        )

    def add_dest(self, d, func):
        self._dest_funcs[d] = func

    def add_name(self, func):
        self._name_funcs.append(func)

    def command(self, name):
        return self._commands[name]

    @staticmethod
    def instance():
        if not hasattr(_Funcs, "_instance"):
            _Funcs._instance = _Funcs()
        return _Funcs._instance


def _files(path):
    abspath = os.path.abspath(path)
    for root, _, files in os.walk(abspath):
        for fname in files:
            yield root, fname


def _dryrun(srcpath, dstpath):
    print "FROM", srcpath
    print "TO  ", dstpath


def _exec_command(cmd, srcpath, dstpath):
    _dryrun(srcpath, dstpath)

    head, _ = os.path.split(dstpath)
    try:
        os.makedirs(head)
    except os.error:
        pass
    try:
        _Funcs.instance().command(cmd)(srcpath, dstpath)
    except OSError as e:
        print str(e)


def _start_impl(cmd, src, dst):
    files = [(r, f) for r, f in _files(src)]
    funcs = _Funcs.instance()

    # Loop for all files and all destinations
    for dstdir, func in funcs._dest_funcs.iteritems():
        for root, filename in files:
            if func(root, filename):
                newname = funcs._name_funcs[-1](root, filename)
                dstpath = os.path.join(dst, dstdir, newname)
                srcpath = os.path.join(root, filename)
                if FLAGS.dryrun:
                    _dryrun(srcpath, dstpath)
                else:
                    _exec_command(cmd, srcpath, dstpath)


def name(func):
    """Decorator for name conversion.

    Decorated function takes two arguments 'root' and 'filename' and returns
    new filename.

    Args:
        func name conversion.
    """
    _Funcs.instance().add_name(func)
    return func


def dest(d):
    """Decorator for destination.

    Decorated function takes two arguments 'root' and 'filename' and returns
    boolean value.

    Args:
        d dirname
    """
    def wrap(func):
        _Funcs.instance().add_dest(d, func)
    return wrap


def start(argv):
    """Start walkdo.

    Args:
        argv: sys.argv
    """
    FLAGS(argv)
    _start_impl(FLAGS.cmd, FLAGS.src, FLAGS.dest)
