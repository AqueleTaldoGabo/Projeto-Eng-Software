
{
  description = "Ambiente de desenvolvimento Pesquisa-Operacional";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in {
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = [
          pkgs.python3
          pkgs.python313Packages.fastapi
          pkgs.python313Packages.pydantic
          pkgs.python313Packages.uvicorn
          pkgs.python313Packages.sqlalchemy
          pkgs.python313Packages.psycopg2
          pkgs.python313Packages.jinja2
          pkgs.docker
          pkgs.docker-compose
          pkgs.dbeaver-bin
        ];

        shellHook = ''
          echo "Ambiente de Desenvolvimento Engenharia-do-Software carregado!"
          echo "Python: $(python --version)"
        '';
      };
    };
}
