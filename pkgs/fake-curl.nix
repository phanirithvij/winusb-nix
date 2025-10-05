{ pkgs, ... }:
pkgs.runCommand "fake-curl" { } ''
  mkdir -p $out/bin
  substitute ${./fake-curl.sh} $out/bin/curl \
    --subst-var-by curl ${pkgs.curl}
  chmod +x $out/bin/curl
''
