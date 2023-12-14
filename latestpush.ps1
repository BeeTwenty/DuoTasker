


# Build the Docker image
docker build --no-cache -t duotasker:latest .

# Tag the image
docker tag duotasker:latest beetwenty/duotasker:latest

# Push the image to Docker Hub or your private registry
docker push beetwenty/duotasker:latest