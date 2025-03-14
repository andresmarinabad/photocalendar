FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    texlive-base \
    texlive-latex-base \
    texlive-fonts-recommended \
    texlive-xetex \
    texlive-pictures \
    texlive-latex-recommended \
    texlive-fonts-extra \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY build/calendar.sty build/calendar.sty
COPY data/.keep data/.keep
COPY images/.keep images/.keep
COPY input/.keep input/.keep
COPY output/.keep output/.keep
COPY templates/header templates/header

COPY src/ src/

RUN pip install --no-cache-dir -r src/requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]