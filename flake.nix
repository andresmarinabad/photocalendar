{
  description = "PhotoCalendar: FastAPI + React + TeX Live";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
  };

  outputs = { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
      calendarTex = pkgs.texlive.combine {
        inherit (pkgs.texlive)
          scheme-basic
          xcolor
          clock
          ifsym
          graphics # graphicx
          marvosym
          geometry
          psnfss # palatino.sty
          palatino # Palatino font files
          tools # tabularx, used by build/calendar.sty
          mwe; # example-image fallback for months without a photo
      };
    in {
      devShells.${system}.default = pkgs.mkShell {
        packages = with pkgs; [
          uv
          nodejs_22
          calendarTex
          stdenv.cc.cc.lib
          zlib
        ];

        shellHook = ''
          export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath [
            pkgs.stdenv.cc.cc.lib
            pkgs.zlib
          ]}''${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
          echo "PhotoCalendar — entorno listo (uv + Node 22 + TeX Live)."
          echo ""
          echo "  Primera vez:  make install"
          echo "  Arrancar:     make start   →  http://localhost:8000"
          echo ""
          echo "  Desarrollo frontend (hot-reload, 2 terminales):"
          echo "    make dev-backend   (terminal 1)"
          echo "    make dev-frontend  (terminal 2)  →  http://localhost:5173"
          echo ""
          echo "  Migrar CSVs de input/ (tras arrancar):"
          echo "    curl -X POST 'http://localhost:8000/api/migrate/csv?year=2027'"
        '';
      };
    };
}
