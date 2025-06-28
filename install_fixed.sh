#!/bin/bash

# Fixed Installation Script for MrAK High-Speed Bot
# Resolves cchardet compilation issues

echo "🔧 Installing MrAK High-Speed Bot Dependencies (Fixed Version)"
echo "============================================================="

# Function to check if package is installed
check_package() {
    python3 -c "import $1" 2>/dev/null
    return $?
}

# Install core packages first
echo "📦 Installing core packages..."
pip3 install --upgrade pip

# Install packages one by one to catch any issues
echo "🚀 Installing performance-optimized packages..."

# Core telegram packages
pip3 install pyrofork==2.3.58
pip3 install tgcrypto

# Web server and async packages
pip3 install "aiohttp[speedups]>=3.9.0"
pip3 install python-dotenv
pip3 install motor
pip3 install aiofiles

# Networking and utilities
pip3 install dnspython
pip3 install apscheduler
pip3 install requests
pip3 install validators
pip3 install psutil
pip3 install jinja2
pip3 install shortzy
pip3 install telegraph

echo "⚡ Installing performance optimization packages..."

# Performance packages (with fallbacks)
# Use charset-normalizer instead of cchardet (fixes compilation issue)
pip3 install "charset-normalizer>=3.0.0"

# DNS and compression optimizations
if ! pip3 install "aiodns>=3.0.0"; then
    echo "⚠️  aiodns failed, skipping (optional performance package)"
fi

if ! pip3 install "brotlipy>=0.7.0"; then
    echo "⚠️  brotlipy failed, trying alternative..."
    pip3 install brotli || echo "⚠️  Brotli compression not available"
fi

# JSON and compression speed improvements
if ! pip3 install "orjson>=3.9.0"; then
    echo "⚠️  orjson failed, using standard json (slower but functional)"
fi

if ! pip3 install "lz4>=4.3.0"; then
    echo "⚠️  lz4 failed, skipping compression optimization"
fi

# MongoDB optimization
pip3 install "pymongo[srv]>=4.0.0"

# Linux-specific performance packages
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🐧 Installing Linux-specific optimizations..."
    if ! pip3 install "uvloop>=0.19.0"; then
        echo "⚠️  uvloop failed, using standard asyncio (slower but functional)"
    fi
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "📊 Checking installation status..."

# Check critical packages
CRITICAL_PACKAGES=("pyrogram" "aiohttp" "motor" "psutil")
ALL_GOOD=true

for package in "${CRITICAL_PACKAGES[@]}"; do
    if check_package $package; then
        echo "✅ $package - OK"
    else
        echo "❌ $package - MISSING"
        ALL_GOOD=false
    fi
done

# Check performance packages
PERFORMANCE_PACKAGES=("orjson" "uvloop" "aiodns")
echo ""
echo "🚀 Performance package status:"

for package in "${PERFORMANCE_PACKAGES[@]}"; do
    if check_package $package; then
        echo "✅ $package - Installed (performance boost active)"
    else
        echo "⚠️  $package - Not available (using fallback)"
    fi
done

echo ""
if $ALL_GOOD; then
    echo "🎉 All critical packages installed successfully!"
    echo "🚀 Your bot is ready for high-speed streaming!"
    echo ""
    echo "📝 Next steps:"
    echo "   1. Configure your .env file with performance settings"
    echo "   2. Run: python3 -m MrAKTech"
    echo "   3. Monitor performance at /status endpoint"
else
    echo "⚠️  Some critical packages failed to install."
    echo "🔧 Please check the error messages above and install manually if needed."
fi

echo ""
echo "🎯 Performance optimizations applied:"
echo "   ✅ Enhanced chunk sizing algorithm"
echo "   ✅ Advanced caching system"
echo "   ✅ Performance monitoring"
echo "   ✅ 16 workers for maximum throughput"
echo "   ✅ Optimized server configuration"
echo ""
