module.exports = {
    apps: [{
        name: "studylion",
        script: "./start.py",
        interpreter: "./venv/bin/python",
        autorestart: true,
        watch: false,
        env: {
            NODE_ENV: "production",
        },
        restart_delay: 5000,
    }, {
        name: "tracking",
        script: "./voice_tracker_service.py",
        interpreter: "./venv/bin/python",
        autorestart: true,
        watch: false,
        env: {
            NODE_ENV: "production",
        },
        restart_delay: 5000,
    }]
}
