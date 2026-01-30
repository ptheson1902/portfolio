#############################################
# Portfolio Deploy to AWS S3
# PowerShell Script for Windows
#############################################

param(
    [Parameter(Mandatory=$false)]
    [string]$BucketName = "",

    [Parameter(Mandatory=$false)]
    [string]$ApiUrl = "",

    [Parameter(Mandatory=$false)]
    [switch]$SkipBuild = $false
)

# Colors
$Green = "Green"
$Yellow = "Yellow"
$Red = "Red"
$Blue = "Cyan"

Write-Host ""
Write-Host "=======================================" -ForegroundColor $Blue
Write-Host "  Portfolio Deploy to AWS S3" -ForegroundColor $Blue
Write-Host "=======================================" -ForegroundColor $Blue
Write-Host ""

# Get script directory and project root
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$FrontendDir = Join-Path $ProjectRoot "frontend"

# Check if AWS CLI is installed
Write-Host "[1/5] Checking AWS CLI..." -ForegroundColor $Yellow
try {
    $awsVersion = aws --version 2>&1
    Write-Host "  AWS CLI: $awsVersion" -ForegroundColor $Green
} catch {
    Write-Host "  ERROR: AWS CLI not installed!" -ForegroundColor $Red
    Write-Host "  Install: https://aws.amazon.com/cli/" -ForegroundColor $Yellow
    exit 1
}

# Check AWS credentials
Write-Host "[2/5] Checking AWS credentials..." -ForegroundColor $Yellow
try {
    $identity = aws sts get-caller-identity 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Not configured"
    }
    Write-Host "  AWS credentials OK" -ForegroundColor $Green
} catch {
    Write-Host "  ERROR: AWS credentials not configured!" -ForegroundColor $Red
    Write-Host "  Run: aws configure" -ForegroundColor $Yellow
    exit 1
}

# Get bucket name if not provided
if ([string]::IsNullOrEmpty($BucketName)) {
    $BucketName = Read-Host "Enter S3 bucket name"
}

# Get API URL if not provided
if ([string]::IsNullOrEmpty($ApiUrl)) {
    Write-Host ""
    Write-Host "Enter your backend API URL (e.g., http://your-ec2-ip or https://api.yourdomain.com)" -ForegroundColor $Yellow
    $ApiUrl = Read-Host "API URL"
}

# Validate inputs
if ([string]::IsNullOrEmpty($BucketName)) {
    Write-Host "ERROR: Bucket name is required!" -ForegroundColor $Red
    exit 1
}

Write-Host ""
Write-Host "Configuration:" -ForegroundColor $Blue
Write-Host "  Bucket: $BucketName" -ForegroundColor $Green
Write-Host "  API URL: $ApiUrl" -ForegroundColor $Green
Write-Host ""

# Build frontend
if (-not $SkipBuild) {
    Write-Host "[3/5] Building frontend..." -ForegroundColor $Yellow

    # Create .env.production
    $envFile = Join-Path $FrontendDir ".env.production"
    @"
VITE_API_URL=$ApiUrl
"@ | Out-File -FilePath $envFile -Encoding utf8

    Write-Host "  Created .env.production" -ForegroundColor $Green

    # Navigate to frontend and build
    Push-Location $FrontendDir
    try {
        Write-Host "  Installing dependencies..." -ForegroundColor $Yellow
        npm install

        Write-Host "  Building..." -ForegroundColor $Yellow
        npm run build

        if ($LASTEXITCODE -ne 0) {
            throw "Build failed"
        }
        Write-Host "  Build complete!" -ForegroundColor $Green
    } catch {
        Write-Host "  ERROR: Build failed!" -ForegroundColor $Red
        Pop-Location
        exit 1
    }
    Pop-Location
} else {
    Write-Host "[3/5] Skipping build (--SkipBuild)" -ForegroundColor $Yellow
}

# Check if bucket exists, create if not
Write-Host "[4/5] Checking S3 bucket..." -ForegroundColor $Yellow
$bucketExists = aws s3api head-bucket --bucket $BucketName 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  Bucket does not exist. Creating..." -ForegroundColor $Yellow

    # Get default region
    $region = aws configure get region
    if ([string]::IsNullOrEmpty($region)) {
        $region = "ap-northeast-1"
    }

    # Create bucket
    if ($region -eq "us-east-1") {
        aws s3api create-bucket --bucket $BucketName
    } else {
        aws s3api create-bucket --bucket $BucketName --create-bucket-configuration LocationConstraint=$region
    }

    # Enable static website hosting
    aws s3 website "s3://$BucketName" --index-document index.html --error-document index.html

    # Set bucket policy for public access
    $policy = @"
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::$BucketName/*"
        }
    ]
}
"@

    # Disable block public access
    aws s3api put-public-access-block --bucket $BucketName --public-access-block-configuration "BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false"

    # Apply bucket policy
    $policy | aws s3api put-bucket-policy --bucket $BucketName --policy file:///dev/stdin

    Write-Host "  Bucket created and configured!" -ForegroundColor $Green
} else {
    Write-Host "  Bucket exists" -ForegroundColor $Green
}

# Upload to S3
Write-Host "[5/5] Uploading to S3..." -ForegroundColor $Yellow
$distDir = Join-Path $FrontendDir "dist"

# Sync files
aws s3 sync $distDir "s3://$BucketName" --delete

# Set cache headers for assets
aws s3 cp "s3://$BucketName" "s3://$BucketName" --recursive --exclude "*" --include "*.js" --include "*.css" --metadata-directive REPLACE --cache-control "max-age=31536000"
aws s3 cp "s3://$BucketName" "s3://$BucketName" --recursive --exclude "*" --include "*.html" --metadata-directive REPLACE --cache-control "no-cache"

Write-Host "  Upload complete!" -ForegroundColor $Green

# Get website URL
$region = aws configure get region
if ([string]::IsNullOrEmpty($region)) {
    $region = "ap-northeast-1"
}
$websiteUrl = "http://$BucketName.s3-website-$region.amazonaws.com"

Write-Host ""
Write-Host "=======================================" -ForegroundColor $Green
Write-Host "  DEPLOYMENT COMPLETE!" -ForegroundColor $Green
Write-Host "=======================================" -ForegroundColor $Green
Write-Host ""
Write-Host "Website URL:" -ForegroundColor $Blue
Write-Host "  $websiteUrl" -ForegroundColor $Green
Write-Host ""
Write-Host "S3 Console:" -ForegroundColor $Blue
Write-Host "  https://s3.console.aws.amazon.com/s3/buckets/$BucketName" -ForegroundColor $Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor $Yellow
Write-Host "  1. Deploy backend to EC2 (run scripts/deploy.sh on EC2)" -ForegroundColor $Yellow
Write-Host "  2. Update backend CORS_ORIGINS to include S3 URL" -ForegroundColor $Yellow
Write-Host "  3. (Optional) Add CloudFront for HTTPS and CDN" -ForegroundColor $Yellow
Write-Host ""
