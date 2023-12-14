


# Build the Docker image
docker build --no-cache -t duotasker:dev .

# Tag the image
docker tag duotasker:dev beetwenty/duotasker:dev

# Push the image to Docker Hub or your private registry
docker push beetwenty/duotasker:dev
