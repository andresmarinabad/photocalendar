{
  description = "PhotoCalendar: Streamlit, uv, TeX Live y SQLite";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
  };

  outputs = { self, nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in {
      devShells.${system}.default = pkgs.mkShell {
        packages = with pkgs; [
          uv
          texlive.combined.scheme-full
          sqlite
          stdenv.cc.cc.lib
          zlib
        ];

        shellHook = ''
          export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath [
            pkgs.stdenv.cc.cc.lib
            pkgs.zlib
          ]}''${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
          echo "PhotoCalendar — entorno listo (uv + TeX Live + sqlite)."
          echo "  uv sync"
          echo "  uv run streamlit run src/app.py"
          echo "Opcional: YEAR=2026 uv run streamlit run src/app.py"
        '';
      };
    };
}
