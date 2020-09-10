set -e
echo "deploy | start"

cd "$(dirname $0)"

sam build --use-container --debug

sam deploy \
    --stack-name "resy" \
    --s3-bucket "resy-cf" \
    --capabilities "CAPABILITY_IAM" \
    --tags "team=resy"

echo "deploy | done"
