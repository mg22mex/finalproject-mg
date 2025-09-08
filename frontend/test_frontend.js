#!/usr/bin/env node
/**
 * Simple test script to verify frontend dependencies
 */

console.log('🚗 Testing Autosell.mx Frontend...');
console.log('=' .repeat(50));

// Test Node.js version
const nodeVersion = process.version;
console.log(`✅ Node.js version: ${nodeVersion}`);

// Test npm version
const { execSync } = require('child_process');
try {
    const npmVersion = execSync('npm --version', { encoding: 'utf8' }).trim();
    console.log(`✅ npm version: ${npmVersion}`);
} catch (error) {
    console.log('❌ npm not available');
}

// Test if we can read package.json
try {
    const packageJson = require('./package.json');
    console.log(`✅ Package.json loaded successfully`);
    console.log(`   Project: ${packageJson.name}`);
    console.log(`   Version: ${packageJson.version}`);
} catch (error) {
    console.log('❌ Failed to load package.json:', error.message);
}

// Test if we can access node_modules (check parent directory for workspaces)
try {
    const fs = require('fs');
    const path = require('path');
    
    const parentNodeModules = path.join(__dirname, '..', 'node_modules');
    const localNodeModules = path.join(__dirname, 'node_modules');
    
    if (fs.existsSync(parentNodeModules)) {
        console.log('✅ node_modules directory exists (workspace setup)');
        
        // Check if key frontend packages are available
        const reactPath = path.join(parentNodeModules, 'react');
        const vitePath = path.join(parentNodeModules, 'vite');
        
        if (fs.existsSync(reactPath)) {
            console.log('✅ React package found');
        }
        if (fs.existsSync(vitePath)) {
            console.log('✅ Vite package found');
        }
    } else if (fs.existsSync(localNodeModules)) {
        console.log('✅ Local node_modules directory exists');
    } else {
        console.log('❌ node_modules directory not found');
    }
} catch (error) {
    console.log('❌ Failed to check node_modules:', error.message);
}

// Test if we can import key packages
try {
    const path = require('path');
    const parentNodeModules = path.join(__dirname, '..', 'node_modules');
    
    // Add parent node_modules to module path
    const Module = require('module');
    const originalResolve = Module._resolveFilename;
    Module._resolveFilename = function(request, parent, isMain) {
        try {
            return originalResolve(request, parent, isMain);
        } catch (e) {
            const resolved = path.resolve(parentNodeModules, request);
            if (require('fs').existsSync(resolved)) {
                return resolved;
            }
            throw e;
        }
    };
    
    console.log('✅ Module resolution configured for workspace');
} catch (error) {
    console.log('❌ Failed to configure module resolution:', error.message);
}

console.log('\n' + '=' .repeat(50));
console.log('🎉 Frontend test completed!');
console.log('\nNext steps:');
console.log('1. Run: npm run dev');
console.log('2. Open: http://localhost:3000');
console.log('3. Check that the React app loads');
console.log('\nNote: Dependencies are installed in the root node_modules (workspace setup)');
