docker build -t hw2 $(pwd)
docker run --mount src=$(pwd)/hw_2/artifacts,target=/hw_2/artifacts,type=bind -it hw2