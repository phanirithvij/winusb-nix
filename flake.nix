{
  description = "Quickemu automation shell";

  inputs.nixpkgs.url = "github:phanirithvij/nixpkgs/quickemu-patched";

  outputs =
    inputs:
    let
      system = "x86_64-linux";
      pkgs = inputs.nixpkgs.legacyPackages.${system};
      python' = pkgs.python3.withPackages (
        ps: with ps; [
          pillow
          imagehash
          ansible-core
        ]
      );
      fake-curl = pkgs.callPackage ./pkgs/fake-curl.nix { };
      quickemu' = pkgs.quickemu.override {
        curl = fake-curl;
      };
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = with pkgs; [
          python'
          quickemu'
          spice-gtk # optional, for spicy and --display none
          openssh
          sshpass
          ansible
          ansible-navigator
        ];
      };
    };
}
