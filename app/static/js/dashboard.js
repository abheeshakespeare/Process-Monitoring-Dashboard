document.addEventListener('DOMContentLoaded', () => {
    // Dark Mode Toggle
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    const themeIcon = document.getElementById('theme-icon');

    function toggleDarkMode() {
        document.documentElement.classList.toggle('dark');
        localStorage.setItem('dark-mode', document.documentElement.classList.contains('dark'));
        themeIcon.classList.toggle('fa-moon');
        themeIcon.classList.toggle('fa-sun');
    }

    // Check saved preference
    if (localStorage.getItem('dark-mode') === 'true') {
        document.documentElement.classList.add('dark');
        themeIcon.classList.remove('fa-moon');
        themeIcon.classList.add('fa-sun');
    }

    darkModeToggle.addEventListener('click', toggleDarkMode);

    

    // Process search
    const processSearch = document.getElementById('process-search');
    processSearch.addEventListener('input', filterProcesses);


    const memoryChart = new Chart(document.getElementById('memory-chart'), {
        type: 'bar',
        data: {
            labels: ['Used', 'Available', 'Total'],
            datasets: [{
                label: 'Memory Usage (MB)',
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
                data: [0, 0, 0]
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Memory (MB)'
                    }
                }
            },
            animation: {
                duration: 1000,  // Smooth transitions
                easing: 'easeInOutQuart'
            }
        }
    });

    function updateMemoryCard(memoryData) {
        const memoryDetails = document.getElementById('memory-details');
        memoryDetails.innerHTML = `
            Used: ${memoryData.used.toFixed(2)} MB 
            | Total: ${memoryData.total.toFixed(2)} MB 
            | ${memoryData.percent.toFixed(2)}%
        `;

        // Update bar chart with dynamic memory data
        memoryChart.data.datasets[0].data = [
            memoryData.used,
            memoryData.available,
            memoryData.total
        ];
        memoryChart.update();
    }

    function updateProcessesTable(processes) {
        const processesList = document.getElementById('processes-list');
        processesList.innerHTML = processes.map(process => `
            <tr class="border-b dark:border-gray-700">
                <td class="p-3">${process.pid}</td>
                <td class="p-3">${process.name}</td>
                <td class="p-3">${process.user}</td>
                <td class="p-3">${process.cpu_usage.toFixed(2)}%</td>
                <td class="p-3">${process.memory_usage.toFixed(2)}%</td>
                <td class="p-3">
                    <select 
                        onchange="setPriority(${process.pid}, this.value)" 
                        class="px-2 py-1 rounded bg-gray-100 dark:bg-gray-700"
                    >
                        <option value="low" ${process.priority === 'Low' ? 'selected' : ''}>Low</option>
                        <option value="normal" ${process.priority === 'Normal' ? 'selected' : ''}>Normal</option>
                        <option value="high" ${process.priority === 'High' ? 'selected' : ''}>High</option>
                    </select>
                </td>
                <td class="p-3">
                    <button 
                        onclick="killProcess(${process.pid})" 
                        class="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600"
                    >
                        Terminate
                    </button>
                </td>
            </tr>
        `).join('');
    }

    function setPriority(pid, priority) {
        fetch('/api/process/priority', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ pid, priority })
        })
        .then(response => response.json())
        .then(result => {
            if (result.status === 'success') {
                console.log(`Process ${pid} priority set to ${priority}`);
            } else {
                alert(`Failed to set priority: ${result.message}`);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to set process priority');
        });
    }


    // Fetch and update system data
    function fetchSystemData() {
        Promise.all([
            fetch('/api/performance').then(res => res.json()),
            fetch('/api/system-info').then(res => res.json()),
            fetch('/api/processes').then(res => res.json())
        ]).then(([performance, systemInfo, processes]) => {
            updateCPUCard(performance.cpu, performance.performance_history.cpu);
            updateMemoryCard(performance.memory);
            updateSystemInfoCard(systemInfo);
            updateProcessesTable(processes);
        }).catch(error => {
            console.error('Error fetching system data:', error);
        });
    }

    function createLineChart(canvasId, label, color) {
        const ctx = document.getElementById(canvasId).getContext('2d');
        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: Array(50).fill(''),
                datasets: [{
                    label: label,
                    data: [],
                    borderColor: color,
                    tension: 0.4,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                    y: { beginAtZero: true, max: 100 }
                }
            }
        });
    }

    function updateCPUCard(cpuData, cpuHistory) {
        const cpuDetails = document.getElementById('cpu-details');
        cpuDetails.innerHTML = `
            Current: ${cpuData.overall_usage.toFixed(2)}% 
            | Frequency: ${cpuData.current_freq.toFixed(2)} MHz
        `;

        cpuChart.data.datasets[0].data = cpuHistory;
        cpuChart.update();
    }

    function updateMemoryCard(memoryData) {
        const memoryDetails = document.getElementById('memory-details');
        memoryDetails.innerHTML = `
            Used: ${memoryData.used.toFixed(2)} MB 
            | Total: ${memoryData.total.toFixed(2)} MB 
            | ${memoryData.percent.toFixed(2)}%
        `;

        memoryChart.data.datasets[0].data = Array(50).fill(memoryData.percent);
        memoryChart.update();
    }

    function updateSystemInfoCard(systemInfo) {
        const systemInfoDetails = document.getElementById('system-info-details');
        systemInfoDetails.innerHTML = `
            <p>OS: ${systemInfo.os} ${systemInfo.release}</p>
            <p>Processor: ${systemInfo.processor}</p>
            <p>Cores: ${systemInfo.total_cores} | Threads: ${systemInfo.total_threads}</p>
            <p>Total Memory: ${systemInfo.total_memory.toFixed(2)} MB</p>
        `;
    }

    function updateProcessesTable(processes) {
        const processesList = document.getElementById('processes-list');
        processesList.innerHTML = processes.map(process => `
            <tr class="border-b dark:border-gray-700">
                <td class="p-3">${process.pid}</td>
                <td class="p-3">${process.name}</td>
                <td class="p-3">${process.user}</td>
                <td class="p-3">${process.cpu_usage.toFixed(2)}%</td>
                <td class="p-3">${process.memory_usage.toFixed(2)}%</td>
                <td class="p-3">
                    <button 
                        onclick="killProcess(${process.pid})" 
                        class="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600"
                    >
                        Terminate
                    </button>
                </td>
            </tr>
        `).join('');
    }

    function filterProcesses() {
        const searchTerm = processSearch.value.toLowerCase();
        const rows = document.querySelectorAll('#processes-list tr');
        rows.forEach(row => {
            const processName = row.cells[1].textContent.toLowerCase();
            const processPid = row.cells[0].textContent;
            row.style.display = 
                processName.includes(searchTerm) || 
                processPid.includes(searchTerm) ? '' : 'none';
        });
    }

    function killProcess(pid) {
        fetch('/api/process/kill', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ pid })
        })
        .then(response => response.json())
        .then(result => {
            if (result.status === 'success') {
                alert(`Process ${pid} terminated successfully`);
                fetchSystemData();  // Refresh processes
            } else {
                alert(`Failed to terminate process: ${result.message}`);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to terminate process');
        });
    }

    // Initial data fetch and periodic updates
    fetchSystemData();
    setInterval(fetchSystemData, 5000);  // Update every 5 seconds
});