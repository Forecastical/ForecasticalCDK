{
  inputs = {
    #nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs";
    systems.url = "github:nix-systems/default";
  };

  outputs =
    { systems, nixpkgs, ... }@inputs:
    let
      eachSystem = f: nixpkgs.lib.genAttrs (import systems) (system: f nixpkgs.legacyPackages.${system});
    in
    {
      packages = eachSystem (pkgs: {
      });

      devShells = eachSystem (pkgs: {
        default = pkgs.mkShell {
          buildInputs = with pkgs; [
            # Add development dependencies here
            nodejs_22
            nodePackages_latest.aws-cdk
            typescript
            nodePackages_latest.typescript-language-server
          ];
        };
      });
    };
}
