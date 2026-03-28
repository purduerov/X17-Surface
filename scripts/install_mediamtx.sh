# Check if mediamtx executable exists in /ros/mediamtx
if [ ! -f ./ros/mediamtx_node/src/mediamtx ]; then
    # Determine architecture
    # If arch is amd64 (x86_64), download the amd64 version
    # If arch is arm64 (aarch64), download the arm64 version

    # 1. Download the tar.gz file
    echo "Downloading mediamtx..."
    arch=$(uname -m)
    if [ "$arch" == "x86_64" ]; then
        echo "Architecture: amd64"
        wget https://github.com/bluenviron/mediamtx/releases/download/v1.11.1/mediamtx_v1.11.1_linux_amd64.tar.gz

        # 3. Extract only the mediamtx executable
        echo "Extracting the mediamtx executable..."
        tar -xvzf mediamtx_v1.11.1_linux_amd64.tar.gz -K mediamtx

        # 4. Move the mediamtx binary to the target directory
        echo "Moving mediamtx"
        mv mediamtx ./ros/mediamtx_node/src/

        # (Optional) 5. Cleanup
        echo "Cleaning up..."
        rm mediamtx_v1.11.1_linux_amd64.tar.gz

    elif [ "$arch" == "aarch64" ]; then
        echo "Architecture: arm64"
        wget https://github.com/bluenviron/mediamtx/releases/download/v1.11.1/mediamtx_v1.11.1_linux_arm64v8.tar.gz

        # 3. Extract only the mediamtx executable
        echo "Extracting the mediamtx executable..."
        tar -xvzf mediamtx_v1.11.1_linux_arm64v8.tar.gz -K mediamtx

        # 4. Move the mediamtx binary to the target directory
        echo "Moving mediamtx"
        mv mediamtx ./ros/mediamtx_node/src/

        # # (Optional) 5. Cleanup
        echo "Cleaning up..."
        rm mediamtx_v1.11.1_linux_arm64v8.tar.gz
    else
        echo "Unsupported architecture: $arch"
        exit 1
    fi

    echo "Done!"
else
    echo "mediamtx executable found in ./ros/mediamtx_node/src"
fi