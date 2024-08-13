mkdir -p ~/.streamlit/

echo "\
    [general]\n\
    email = \"pdas2006@gmail.com\"\n\
    " > ~/.streamlit/credentials.toml

echo "\
    [server]\n\
    headless = true\n\
    enableCORS = false
    port = $PORT\n\
    " > ~/.streamlit/config.toml
