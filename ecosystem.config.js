module.exports = {
    apps: [{
        name: "studylion",
        script: "./start.py",
        interpreter: "./venv/bin/python",
        autorestart: true,
        watch: false,
        env: {
            NODE_ENV: "production",
        }
    }]
}
