{pkgs}: {
  deps = [
    pkgs.glibcLocales
    pkgs.openssl
    pkgs.gitFull
    pkgs.pkg-config
    pkgs.libffi
    pkgs.gdb
    pkgs.cacert
    pkgs.rustc
    pkgs.libiconv
    pkgs.cargo
    pkgs.zeromq
    pkgs.libxcrypt
    pkgs.unixODBC
  ];
}
