{ stdenv, foo, bar ? false, ... }:

/*
 * foo
 */

let
  a = 1; # just a comment
  b = null;
  c = toString 10;
in stdenv.mkDerivation rec {
  name = "foo-${version}";
  version = "1.3";

  configureFlags = [ "--with-foo2" ] ++ stdenv.lib.optional bar "--with-foo=${ with stdenv.lib; foo }"

  postInstall = ''
    ${ if true then "--${test}" else false }
  '';

  meta = with stdenv.lib; {
    homepage = https://nixos.org;
  };
}