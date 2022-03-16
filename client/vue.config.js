const path = require('path')

const BundleTracker = require("webpack-bundle-tracker")


const SERVER_INTEGRATION = true

const PUBLIC_PATH = SERVER_INTEGRATION ? '/static/' : './'
const OUTPUT_PATH = SERVER_INTEGRATION ? '../server/public/client/' : './client/'
const BUNDLE_PATH = SERVER_INTEGRATION ? '../server/public/client-files.json' : './client-files.json'

module.exports = {
    pages: {
        index: 'src/core/main.js'
    },
    css: {
        loaderOptions: {
            stylus: {
                import: '~@/styles/var.styl',
            }
        }
    },
    outputDir: OUTPUT_PATH,
    publicPath: process.env.NODE_ENV == 'production' ? PUBLIC_PATH : "http://localhost:8080/",
    devServer: {
        // public: 'localhost:8080',
        headers: {
            "Access-Control-Allow-Origin": "*"
        },
    },
    configureWebpack: {
        plugins: [
            new BundleTracker({ filename: BUNDLE_PATH }),
        ],
        resolve: {
            extensions: ['*', '.js', '.jsx', '.vue'],
            symlinks: false,
            alias: {
                'components': path.resolve(__dirname, 'src/components'),
                'pages': path.resolve(__dirname, 'src/pages'),
                'images': path.resolve(__dirname, 'src/assets/images'),
                '@': path.resolve(__dirname, 'src'),
                'vue$': 'vue/dist/vue.esm-bundler.js',
                vue: path.resolve(__dirname, `./node_modules/vue`)
            }
        }
    },
}
