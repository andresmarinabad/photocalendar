{
  description = "Entorno de desarrollo Streamlit/Ephem";

  inputs = {
    # Fuente de paquetes estables (se recomienda fijar una versión)
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11"; 
  };

  outputs = { self, nixpkgs, ... }: 
    let
      # Definimos el sistema para el que construiremos (ejemplo: x86_64-linux)
      system = "x86_64-linux";
      # Importamos nixpkgs para el sistema definido
      pkgs = import nixpkgs { inherit system; };

      # Definimos el entorno Python con las librerías necesarias
      pythonEnv = pkgs.python3.withPackages (ps: with ps; [
        # Librerías Python requeridas
        streamlit
        ephem
        pandas
      ]);
      
    in {
      # El corazón: El entorno de desarrollo (devShell)
      devShells.${system}.default = pkgs.mkShell {
        # Paquetes disponibles en el shell (PATH)
        packages = [
          pythonEnv
          # Puedes añadir otras herramientas como git, bash, etc., si las necesitas.
          # pkgs.git
          pkgs.texlive.combined.scheme-full
          pkgs.sqlite
	        pkgs.docker
        ];
        
        # Opcional: Un mensaje de bienvenida y las instrucciones
        shellHook = ''
          echo "✅ Entorno de desarrollo listo. Streamlit y Ephem instalados."
          echo "Para ejecutar la app: streamlit run src/app.py"
          echo "Para salir: exit"
        '';
      };
    };
}
