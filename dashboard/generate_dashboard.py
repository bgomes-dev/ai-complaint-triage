import os
import json

def load_evaluation_results():
    """Reads the evaluation results JSON file containing the 50 complaints."""
    json_path = os.path.join("results", "evaluation_results.json")
    
    # Fallback check if script is executed from inside /notebooks or /dashboard
    if not os.path.exists(json_path):
        json_path = os.path.join("..", "results", "evaluation_results.json")
    
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                print(f"✓ Results file loaded successfully: {json_path}")
                print(f"  -> Total complaints found: {len(data.get('complaints', []))}")
                return data
        except Exception as e:
            print(f"⚠️ Error reading JSON file: {e}")
    else:
        print(f"⚠️ Warning: Could not find '{json_path}'. Fallback structure will be used.")
    
    return None

def main():
    # 1. Load the evaluation data from JSON
    real_data = load_evaluation_results()
    
    # Convert real data to formatted JSON string for embedding into JavaScript
    embedded_json_str = json.dumps(real_data, ensure_ascii=False, indent=2) if real_data else "null"

    # 2. Complete HTML, CSS, and JS Dashboard template
    html_content = f"""<!DOCTYPE html>
<html lang="en" class="h-full bg-slate-50">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Complaint Triage & Routing Assistant | Dashboard</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        brand: {{
                            50: '#f0f7ff',
                            100: '#e0effe',
                            500: '#0284c7',
                            600: '#0369a1',
                            700: '#075985',
                            900: '#0c4a6e',
                        }}
                    }}
                }}
            }}
        }}
    </script>
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- Lucide Icons CDN -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        .custom-scrollbar::-webkit-scrollbar {{
            width: 6px;
            height: 6px;
        }}
        .custom-scrollbar::-webkit-scrollbar-track {{
            background: #f1f5f9;
        }}
        .custom-scrollbar::-webkit-scrollbar-thumb {{
            background: #cbd5e1;
            border-radius: 3px;
        }}
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {{
            background: #94a3b8;
        }}
    </style>
</head>
<body class="h-full font-sans antialiased text-slate-800 flex flex-col min-h-screen">

    <!-- Main Container -->
    <div class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        
        <!-- 1. HEADER SECTION -->
        <header class="bg-white rounded-2xl shadow-sm border border-slate-200/80 p-6 md:p-8">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
                <div>
                    <div class="flex items-center gap-3">
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-brand-50 text-brand-700 border border-brand-100">
                            Portfolio Project
                        </span>
                        <span class="text-xs text-slate-400 font-mono" id="last-updated">Evaluated: Current Run</span>
                    </div>
                    <h1 class="text-2xl md:text-3xl font-bold text-slate-900 tracking-tight mt-2">
                        AI Complaint Triage & Routing Assistant
                    </h1>
                    <p class="text-sm md:text-base text-slate-600 mt-2 max-w-3xl leading-relaxed">
                        Validation dashboard for an LLM-based banking complaint classification pipeline evaluated against human ground truth. It applies an automated confidence threshold for human-in-the-loop review.
                    </p>
                </div>
                <div class="flex items-center gap-3 self-start md:self-auto bg-slate-50 p-3 rounded-xl border border-slate-100">
                    <div class="p-2.5 bg-brand-500 text-white rounded-lg shadow-sm">
                        <i data-lucide="cpu" class="w-6 h-6"></i>
                    </div>
                    <div>
                        <p class="text-xs text-slate-500 font-medium uppercase tracking-wider">Model Status</p>
                        <p class="text-xs font-semibold text-emerald-600 flex items-center gap-1.5 mt-0.5">
                            <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                            Evaluated & Ready
                        </p>
                    </div>
                </div>
            </div>
        </header>

        <!-- 2. OVERVIEW / KPI CARDS -->
        <section aria-label="KPI Metrics">
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
                <!-- Total Complaints -->
                <div class="bg-white rounded-xl p-5 border border-slate-200/80 shadow-sm hover:shadow-md transition-shadow">
                    <div class="flex items-center justify-between text-slate-500 mb-2">
                        <span class="text-xs font-semibold uppercase tracking-wider">Total</span>
                        <i data-lucide="inbox" class="w-4 h-4 text-slate-400"></i>
                    </div>
                    <p class="text-2xl font-bold text-slate-900" id="kpi-total">--</p>
                    <p class="text-[11px] text-slate-500 mt-1">Processed samples</p>
                </div>

                <!-- Overall Accuracy -->
                <div class="bg-white rounded-xl p-5 border border-slate-200/80 shadow-sm hover:shadow-md transition-shadow">
                    <div class="flex items-center justify-between text-slate-500 mb-2">
                        <span class="text-xs font-semibold uppercase tracking-wider">Overall Acc.</span>
                        <i data-lucide="target" class="w-4 h-4 text-brand-500"></i>
                    </div>
                    <p class="text-2xl font-bold text-slate-900" id="kpi-overall">--</p>
                    <p class="text-[11px] text-emerald-600 font-medium mt-1">Exact match accuracy</p>
                </div>

                <!-- Product Accuracy -->
                <div class="bg-white rounded-xl p-5 border border-slate-200/80 shadow-sm hover:shadow-md transition-shadow">
                    <div class="flex items-center justify-between text-slate-500 mb-2">
                        <span class="text-xs font-semibold uppercase tracking-wider">Product Acc.</span>
                        <i data-lucide="layers" class="w-4 h-4 text-indigo-500"></i>
                    </div>
                    <p class="text-2xl font-bold text-slate-900" id="kpi-product">--</p>
                    <p class="text-[11px] text-slate-500 mt-1"><span id="kpi-product-correct">--</span> correct predictions</p>
                </div>

                <!-- Matter Accuracy -->
                <div class="bg-white rounded-xl p-5 border border-slate-200/80 shadow-sm hover:shadow-md transition-shadow">
                    <div class="flex items-center justify-between text-slate-500 mb-2">
                        <span class="text-xs font-semibold uppercase tracking-wider">Matter Acc.</span>
                        <i data-lucide="git-branch" class="w-4 h-4 text-violet-500"></i>
                    </div>
                    <p class="text-2xl font-bold text-slate-900" id="kpi-matter">--</p>
                    <p class="text-[11px] text-slate-500 mt-1"><span id="kpi-matter-correct">--</span> correct predictions</p>
                </div>

                <!-- Approved -->
                <div class="bg-white rounded-xl p-5 border border-emerald-200/80 bg-emerald-50/20 shadow-sm hover:shadow-md transition-shadow">
                    <div class="flex items-center justify-between text-emerald-700 mb-2">
                        <span class="text-xs font-semibold uppercase tracking-wider">Auto Approved</span>
                        <i data-lucide="check-circle-2" class="w-4 h-4 text-emerald-600"></i>
                    </div>
                    <p class="text-2xl font-bold text-emerald-900" id="kpi-approved">--</p>
                    <p class="text-[11px] text-emerald-700 font-medium mt-1">Straight-through processing</p>
                </div>

                <!-- Needs Review -->
                <div class="bg-white rounded-xl p-5 border border-amber-200/80 bg-amber-50/20 shadow-sm hover:shadow-md transition-shadow">
                    <div class="flex items-center justify-between text-amber-700 mb-2">
                        <span class="text-xs font-semibold uppercase tracking-wider">Needs Review</span>
                        <i data-lucide="alert-circle" class="w-4 h-4 text-amber-600"></i>
                    </div>
                    <p class="text-2xl font-bold text-amber-900" id="kpi-review">--</p>
                    <p class="text-[11px] text-amber-700 font-medium mt-1">Sent to human review</p>
                </div>
            </div>
        </section>

        <!-- 3 & 4. VISUALISATION SECTION (Routing & Classification Charts) -->
        <section class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            <!-- Routing Overview Doughnut Card -->
            <div class="bg-white rounded-2xl shadow-sm border border-slate-200/80 p-6 flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-4">
                        <h2 class="text-base font-bold text-slate-900 flex items-center gap-2">
                            <i data-lucide="git-pull-request" class="w-5 h-5 text-brand-500"></i>
                            Automated Routing Breakdown
                        </h2>
                        <span class="text-xs px-2.5 py-1 rounded-md bg-slate-100 text-slate-700 font-medium border border-slate-200" id="confidence-threshold-badge">
                            Threshold: --%
                        </span>
                    </div>
                    <p class="text-xs text-slate-500 mb-4">
                        Complaints with model confidence below the threshold are routed for human review.
                    </p>
                </div>

                <div class="relative flex justify-center items-center h-48 my-2">
                    <canvas id="routingChart"></canvas>
                </div>

                <div class="grid grid-cols-2 gap-3 pt-4 border-t border-slate-100 text-center">
                    <div class="p-2 rounded-lg bg-emerald-50">
                        <span class="text-xs font-medium text-emerald-800">Approved</span>
                        <p class="text-lg font-bold text-emerald-900" id="routing-approved-pct">--%</p>
                    </div>
                    <div class="p-2 rounded-lg bg-amber-50">
                        <span class="text-xs font-medium text-amber-800">Needs Review</span>
                        <p class="text-lg font-bold text-amber-900" id="routing-review-pct">--%</p>
                    </div>
                </div>
            </div>

            <!-- Classification Performance Bar Chart -->
            <div class="lg:col-span-2 bg-white rounded-2xl shadow-sm border border-slate-200/80 p-6 flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-2">
                        <h2 class="text-base font-bold text-slate-900 flex items-center gap-2">
                            <i data-lucide="bar-chart-3" class="w-5 h-5 text-brand-500"></i>
                            Classification Accuracy Performance
                        </h2>
                        <span class="text-xs text-slate-400">Model vs Ground Truth</span>
                    </div>
                    <p class="text-xs text-slate-500 mb-4">
                        Hierarchical accuracy evaluation across Product level and Matter level classification.
                    </p>
                </div>

                <div class="h-56 relative">
                    <canvas id="performanceChart"></canvas>
                </div>

                <div class="flex items-center justify-around pt-4 border-t border-slate-100 text-xs text-slate-600">
                    <div class="flex items-center gap-2">
                        <span class="w-3 h-3 rounded-sm bg-sky-500"></span>
                        <span>Product Accuracy</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <span class="w-3 h-3 rounded-sm bg-violet-500"></span>
                        <span>Matter Accuracy</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <span class="w-3 h-3 rounded-sm bg-emerald-500"></span>
                        <span>Overall Exact Match</span>
                    </div>
                </div>
            </div>
        </section>

        <!-- NAVIGATION TABS -->
        <div class="border-b border-slate-200">
            <nav class="flex space-x-8" aria-label="Tabs">
                <button onclick="switchTab('all-complaints')" id="tab-all-complaints" class="tab-btn border-brand-500 text-brand-600 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center gap-2">
                    <i data-lucide="table" class="w-4 h-4"></i>
                    All Complaints Table
                </button>
                <button onclick="switchTab('error-analysis')" id="tab-error-analysis" class="tab-btn border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center gap-2">
                    <i data-lucide="alert-triangle" class="w-4 h-4"></i>
                    Error Analysis
                    <span id="error-badge-count" class="ml-1 bg-red-100 text-red-700 py-0.5 px-2 rounded-full text-xs font-semibold">0</span>
                </button>
                <button onclick="switchTab('needs-review')" id="tab-needs-review" class="tab-btn border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center gap-2">
                    <i data-lucide="user-check" class="w-4 h-4"></i>
                    Human Review Queue
                    <span id="review-badge-count" class="ml-1 bg-amber-100 text-amber-800 py-0.5 px-2 rounded-full text-xs font-semibold">0</span>
                </button>
            </nav>
        </div>

        <!-- TAB 1: ALL COMPLAINTS TABLE & FILTERS -->
        <div id="view-all-complaints" class="tab-content space-y-6">
            <!-- Filters Card -->
            <div class="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm space-y-4">
                <div class="flex items-center justify-between border-b border-slate-100 pb-3">
                    <h3 class="text-sm font-semibold text-slate-900 flex items-center gap-2">
                        <i data-lucide="filter" class="w-4 h-4 text-slate-500"></i>
                        Filter Complaints Data
                    </h3>
                    <button onclick="resetFilters()" class="text-xs font-medium text-brand-600 hover:text-brand-700 hover:underline flex items-center gap-1">
                        <i data-lucide="rotate-ccw" class="w-3 h-3"></i> Reset Filters
                    </button>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <!-- Filter: Routing Status -->
                    <div>
                        <label for="filter-routing" class="block text-xs font-medium text-slate-600 mb-1">Routing Status</label>
                        <select id="filter-routing" onchange="applyFilters()" class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg p-2.5 focus:ring-2 focus:ring-brand-500 focus:border-brand-500 text-slate-800 font-medium">
                            <option value="ALL">All Routing Statuses</option>
                            <option value="Approved">Approved Only</option>
                            <option value="Needs Review">Needs Review Only</option>
                        </select>
                    </div>

                    <!-- Filter: Classification Result -->
                    <div>
                        <label for="filter-result" class="block text-xs font-medium text-slate-600 mb-1">Classification Result</label>
                        <select id="filter-result" onchange="applyFilters()" class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg p-2.5 focus:ring-2 focus:ring-brand-500 focus:border-brand-500 text-slate-800 font-medium">
                            <option value="ALL">All Classification Results</option>
                            <option value="Correct">Correct Predictions</option>
                            <option value="Incorrect">Incorrect Predictions (Errors)</option>
                        </select>
                    </div>

                    <!-- Filter: Product (Dynamic) -->
                    <div>
                        <label for="filter-product" class="block text-xs font-medium text-slate-600 mb-1">Product Category</label>
                        <select id="filter-product" onchange="applyFilters()" class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg p-2.5 focus:ring-2 focus:ring-brand-500 focus:border-brand-500 text-slate-800 font-medium">
                            <option value="ALL">All Products</option>
                        </select>
                    </div>
                </div>
            </div>

            <!-- Table Card -->
            <div class="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden">
                <div class="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
                    <span class="text-xs font-medium text-slate-500">
                        Showing <strong id="visible-count" class="text-slate-900">0</strong> of <strong id="total-table-count" class="text-slate-900">0</strong> complaints
                    </span>
                    <span class="text-xs text-slate-400">Click any row to inspect complete details</span>
                </div>

                <div class="overflow-x-auto custom-scrollbar">
                    <table class="w-full text-left border-collapse text-xs">
                        <thead>
                            <tr class="bg-slate-50 border-b border-slate-200/80 text-slate-600 uppercase font-semibold text-[11px] tracking-wider">
                                <th class="py-3.5 px-4 w-16">ID</th>
                                <th class="py-3.5 px-4 w-2/5">Complaint Text</th>
                                <th class="py-3.5 px-4">Predicted Product / Matter</th>
                                <th class="py-3.5 px-4 w-24 text-center">Confidence</th>
                                <th class="py-3.5 px-4 w-28 text-center">Routing</th>
                                <th class="py-3.5 px-4 w-28 text-center">Evaluation</th>
                                <th class="py-3.5 px-4 w-12 text-center">Action</th>
                            </tr>
                        </thead>
                        <tbody id="complaints-table-body" class="divide-y divide-slate-100 text-slate-700">
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB 2: ERROR ANALYSIS SECTION -->
        <div id="view-error-analysis" class="tab-content hidden space-y-6">
            <div class="bg-red-50/50 border border-red-200/80 rounded-2xl p-6">
                <div class="flex items-start gap-3">
                    <div class="p-2 bg-red-100 text-red-700 rounded-lg">
                        <i data-lucide="alert-octagon" class="w-5 h-5"></i>
                    </div>
                    <div>
                        <h3 class="text-base font-bold text-red-900">Classification Error Deep-Dive</h3>
                        <p class="text-xs text-red-700 mt-1">
                            This section isolates all complaints where model prediction disagreed with human ground truth (<code>classification_correct == false</code>).
                        </p>
                    </div>
                </div>
            </div>

            <div id="errors-container" class="grid grid-cols-1 gap-4">
            </div>
        </div>

        <!-- TAB 3: HUMAN-IN-THE-LOOP (NEEDS REVIEW) SECTION -->
        <div id="view-needs-review" class="tab-content hidden space-y-6">
            <div class="bg-amber-50/50 border border-amber-200/80 rounded-2xl p-6">
                <div class="flex items-start gap-3">
                    <div class="p-2 bg-amber-100 text-amber-800 rounded-lg">
                        <i data-lucide="shield-alert" class="w-5 h-5"></i>
                    </div>
                    <div>
                        <h3 class="text-base font-bold text-amber-900">Human-in-the-Loop Review Queue</h3>
                        <p class="text-xs text-amber-800 mt-1">
                            Simulated operational workflow. Complaints with confidence below threshold (<span id="review-threshold-text">--%</span>) require agent validation before actioning.
                        </p>
                    </div>
                </div>
            </div>

            <div id="review-container" class="grid grid-cols-1 gap-4">
            </div>
        </div>

    </div>

    <!-- DETAIL MODAL -->
    <div id="complaint-modal" class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
        <div class="bg-white rounded-2xl shadow-xl border border-slate-200 max-w-2xl w-full overflow-hidden flex flex-col max-h-[90vh]">
            <div class="p-5 border-b border-slate-100 flex items-center justify-between bg-slate-50">
                <div class="flex items-center gap-2">
                    <span class="text-xs font-mono font-bold px-2 py-0.5 bg-slate-200 text-slate-700 rounded" id="modal-id">#000</span>
                    <h3 class="text-sm font-bold text-slate-900">Complaint Details & Evaluation</h3>
                </div>
                <button onclick="closeModal()" class="text-slate-400 hover:text-slate-600 p-1 rounded-lg">
                    <i data-lucide="x" class="w-5 h-5"></i>
                </button>
            </div>
            
            <div class="p-6 overflow-y-auto space-y-6 text-xs leading-relaxed custom-scrollbar">
                <div>
                    <h4 class="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">Original Complaint Text</h4>
                    <div class="p-4 bg-slate-50 border border-slate-200/80 rounded-xl text-slate-800 text-sm italic font-serif" id="modal-text">
                        --
                    </div>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div class="p-4 rounded-xl border border-slate-200 bg-white">
                        <span class="text-[11px] font-bold uppercase tracking-wider text-brand-600 block mb-2">Model Prediction</span>
                        <div class="space-y-1.5">
                            <p><strong class="text-slate-500 font-normal">Product:</strong> <span class="font-semibold text-slate-900" id="modal-pred-product">--</span></p>
                            <p><strong class="text-slate-500 font-normal">Matter:</strong> <span class="font-semibold text-slate-900" id="modal-pred-matter">--</span></p>
                            <p><strong class="text-slate-500 font-normal">Confidence:</strong> <span class="font-semibold text-slate-900" id="modal-pred-conf">--%</span></p>
                        </div>
                    </div>

                    <div class="p-4 rounded-xl border border-slate-200 bg-white">
                        <span class="text-[11px] font-bold uppercase tracking-wider text-slate-500 block mb-2">Human Ground Truth</span>
                        <div class="space-y-1.5">
                            <p><strong class="text-slate-500 font-normal">Product:</strong> <span class="font-semibold text-slate-900" id="modal-truth-product">--</span></p>
                            <p><strong class="text-slate-500 font-normal">Matter:</strong> <span class="font-semibold text-slate-900" id="modal-truth-matter">--</span></p>
                            <p><strong class="text-slate-500 font-normal">Status:</strong> <span id="modal-eval-status">--</span></p>
                        </div>
                    </div>
                </div>

                <div class="flex items-center justify-between p-3 rounded-xl bg-slate-50 border border-slate-100">
                    <span class="text-slate-600">Automated Routing Outcome:</span>
                    <span id="modal-routing-badge">--</span>
                </div>
            </div>

            <div class="p-4 border-t border-slate-100 bg-slate-50 flex justify-end">
                <button onclick="closeModal()" class="px-4 py-2 bg-slate-800 text-white font-medium rounded-lg hover:bg-slate-900 transition-colors">
                    Close
                </button>
            </div>
        </div>
    </div>

    <!-- MAIN JAVASCRIPT LOGIC -->
    <script>
        // Real complaint data injected directly by Python
        const embeddedData = {embedded_json_str};

        let dashboardData = null;
        let chartInstances = {{}};

        document.addEventListener('DOMContentLoaded', () => {{
            fetchData();
        }});

        async function fetchData() {{
            const dataUrl = '../results/evaluation_results.json';
            
            // 1. Attempt to fetch file over HTTP (if hosted on a web server)
            try {{
                const response = await fetch(dataUrl);
                if (response.ok) {{
                    dashboardData = await response.json();
                    initDashboard(dashboardData);
                    return;
                }}
            }} catch (error) {{
                // Fallback silently if fetch fails
            }}

            // 2. If fetch fails (e.g. running under file:// protocol), use embedded data
            if (embeddedData) {{
                dashboardData = embeddedData;
                initDashboard(dashboardData);
            }} else {{
                console.error("No JSON evaluation data found.");
            }}
        }}

        function initDashboard(data) {{
            renderKPIs(data.evaluation, data.routing);
            renderCharts(data.evaluation, data.routing);
            populateProductFilterOptions(data.complaints);
            renderComplaintsTable(data.complaints);
            renderErrorAnalysis(data.complaints);
            renderNeedsReview(data.complaints, data.routing.confidence_threshold);
            lucide.createIcons();
        }}

        function renderKPIs(evalData, routingData) {{
            document.getElementById('kpi-total').textContent = evalData.total_complaints || '--';
            document.getElementById('kpi-overall').textContent = Math.round((evalData.overall_accuracy || 0) * 100) + '%';
            document.getElementById('kpi-product').textContent = Math.round((evalData.product_accuracy || 0) * 100) + '%';
            document.getElementById('kpi-matter').textContent = Math.round((evalData.matter_accuracy || 0) * 100) + '%';
            
            document.getElementById('kpi-product-correct').textContent = evalData.product_correct || 0;
            document.getElementById('kpi-matter-correct').textContent = evalData.matter_correct || 0;

            document.getElementById('kpi-approved').textContent = routingData.approved_count || 0;
            document.getElementById('kpi-review').textContent = routingData.needs_review_count || 0;

            const thresholdPct = Math.round((routingData.confidence_threshold || 0) * 100);
            document.getElementById('confidence-threshold-badge').textContent = `Threshold: ${{thresholdPct}}%`;
            document.getElementById('review-threshold-text').textContent = `${{thresholdPct}}%`;

            const total = evalData.total_complaints || 1;
            document.getElementById('routing-approved-pct').textContent = Math.round((routingData.approved_count / total) * 100) + '%';
            document.getElementById('routing-review-pct').textContent = Math.round((routingData.needs_review_count / total) * 100) + '%';
        }}

        function renderCharts(evalData, routingData) {{
            if (chartInstances.routing) chartInstances.routing.destroy();
            if (chartInstances.performance) chartInstances.performance.destroy();

            const ctxRouting = document.getElementById('routingChart').getContext('2d');
            chartInstances.routing = new Chart(ctxRouting, {{
                type: 'doughnut',
                data: {{
                    labels: ['Auto Approved', 'Needs Review'],
                    datasets: [{{
                        data: [routingData.approved_count, routingData.needs_review_count],
                        backgroundColor: ['#10b981', '#f59e0b'],
                        borderWidth: 0,
                        hoverOffset: 4
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ position: 'bottom', labels: {{ boxWidth: 12, font: {{ size: 11 }} }} }}
                    }},
                    cutout: '70%'
                }}
            }});

            const ctxPerf = document.getElementById('performanceChart').getContext('2d');
            chartInstances.performance = new Chart(ctxPerf, {{
                type: 'bar',
                data: {{
                    labels: ['Product Accuracy', 'Matter Accuracy', 'Overall Accuracy'],
                    datasets: [{{
                        label: 'Accuracy Score (%)',
                        data: [
                            Math.round(evalData.product_accuracy * 100),
                            Math.round(evalData.matter_accuracy * 100),
                            Math.round(evalData.overall_accuracy * 100)
                        ],
                        backgroundColor: ['#0284c7', '#8b5cf6', '#10b981'],
                        borderRadius: 6,
                        barThickness: 32
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        y: {{
                            beginAtZero: true,
                            max: 100,
                            ticks: {{ callback: value => value + '%' }}
                        }},
                        x: {{ grid: {{ display: false }} }}
                    }},
                    plugins: {{
                        legend: {{ display: false }}
                    }}
                }}
            }});
        }}

        function populateProductFilterOptions(complaints) {{
            const select = document.getElementById('filter-product');
            const products = [...new Set(complaints.map(c => c.predicted.product))].sort();
            
            select.innerHTML = '<option value="ALL">All Products</option>';
            products.forEach(prod => {{
                const opt = document.createElement('option');
                opt.value = prod;
                opt.textContent = prod;
                select.appendChild(opt);
            }});
        }}

        function renderComplaintsTable(complaints) {{
            const tbody = document.getElementById('complaints-table-body');
            tbody.innerHTML = '';

            document.getElementById('total-table-count').textContent = complaints.length;
            document.getElementById('visible-count').textContent = complaints.length;

            complaints.forEach(item => {{
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-50/80 cursor-pointer transition-colors';
                tr.onclick = () => openModal(item);

                const isCorrect = item.evaluation.classification_correct;
                const isApproved = item.routing_status === 'Approved';
                const confidencePct = Math.round(item.predicted.confidence * 100);

                tr.innerHTML = `
                    <td class="py-3 px-4 font-mono text-slate-500 font-medium">#${{item.complaint_id}}</td>
                    <td class="py-3 px-4">
                        <p class="line-clamp-2 text-slate-800 leading-snug">${{escapeHtml(item.complaint_text)}}</p>
                    </td>
                    <td class="py-3 px-4">
                        <div class="font-medium text-slate-900">${{escapeHtml(item.predicted.product)}}</div>
                        <div class="text-[11px] text-slate-500">${{escapeHtml(item.predicted.matter)}}</div>
                    </td>
                    <td class="py-3 px-4 text-center">
                        <span class="font-semibold ${{confidencePct < 80 ? 'text-amber-600' : 'text-slate-700'}}">${{confidencePct}}%</span>
                    </td>
                    <td class="py-3 px-4 text-center">
                        <span class="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-semibold ${{isApproved ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'}}">
                            ${{item.routing_status}}
                        </span>
                    </td>
                    <td class="py-3 px-4 text-center">
                        <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-semibold ${{isCorrect ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-red-50 text-red-700 border border-red-200'}}">
                            <i data-lucide="${{isCorrect ? 'check' : 'x'}}" class="w-3 h-3"></i>
                            ${{isCorrect ? 'Correct' : 'Incorrect'}}
                        </span>
                    </td>
                    <td class="py-3 px-4 text-center text-slate-400 hover:text-brand-600">
                        <i data-lucide="eye" class="w-4 h-4 inline"></i>
                    </td>
                `;
                tbody.appendChild(tr);
            }});
        }}

        function applyFilters() {{
            if (!dashboardData) return;

            const routingFilter = document.getElementById('filter-routing').value;
            const resultFilter = document.getElementById('filter-result').value;
            const productFilter = document.getElementById('filter-product').value;

            const filtered = dashboardData.complaints.filter(c => {{
                if (routingFilter !== 'ALL' && c.routing_status !== routingFilter) return false;
                if (resultFilter === 'Correct' && !c.evaluation.classification_correct) return false;
                if (resultFilter === 'Incorrect' && c.evaluation.classification_correct) return false;
                if (productFilter !== 'ALL' && c.predicted.product !== productFilter) return false;
                return true;
            }});

            renderComplaintsTable(filtered);
            lucide.createIcons();
        }}

        function resetFilters() {{
            document.getElementById('filter-routing').value = 'ALL';
            document.getElementById('filter-result').value = 'ALL';
            document.getElementById('filter-product').value = 'ALL';
            applyFilters();
        }}

        function renderErrorAnalysis(complaints) {{
            const errors = complaints.filter(c => !c.evaluation.classification_correct);
            const container = document.getElementById('errors-container');
            document.getElementById('error-badge-count').textContent = errors.length;

            container.innerHTML = '';

            if (errors.length === 0) {{
                container.innerHTML = `
                    <div class="bg-white rounded-xl p-8 text-center text-slate-500 border border-slate-200">
                        <i data-lucide="check-circle" class="w-8 h-8 text-emerald-500 mx-auto mb-2"></i>
                        <p class="font-medium text-sm">No classification errors found in this evaluation run!</p>
                    </div>
                `;
                return;
            }}

            errors.forEach(item => {{
                const card = document.createElement('div');
                card.className = 'bg-white rounded-2xl border border-red-200/80 shadow-sm p-5 hover:shadow-md transition-shadow';
                card.innerHTML = `
                    <div class="flex items-center justify-between border-b border-slate-100 pb-3 mb-3">
                        <div class="flex items-center gap-2">
                            <span class="text-xs font-mono bg-red-100 text-red-800 font-bold px-2 py-0.5 rounded">ID #${{item.complaint_id}}</span>
                            <span class="text-xs text-slate-400">Confidence: ${{Math.round(item.predicted.confidence * 100)}}%</span>
                        </div>
                        <span class="text-xs font-medium px-2.5 py-0.5 rounded-full ${{item.routing_status === 'Approved' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'}}">
                            Routing: ${{item.routing_status}}
                        </span>
                    </div>

                    <div class="mb-4">
                        <span class="text-[11px] uppercase font-semibold text-slate-400 tracking-wider">Complaint Text</span>
                        <p class="text-xs text-slate-800 mt-1 bg-slate-50 p-3 rounded-xl border border-slate-100 italic font-serif">
                            "${{escapeHtml(item.complaint_text)}}"
                        </p>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                        <div class="bg-red-50/60 rounded-xl p-3 border border-red-100">
                            <span class="font-bold text-red-900 block mb-1 flex items-center gap-1">
                                <i data-lucide="x-circle" class="w-3.5 h-3.5 text-red-600"></i> Model Prediction
                            </span>
                            <p><span class="text-slate-500">Product:</span> <strong class="text-slate-800">${{escapeHtml(item.predicted.product)}}</strong></p>
                            <p><span class="text-slate-500">Matter:</span> <strong class="text-slate-800">${{escapeHtml(item.predicted.matter)}}</strong></p>
                        </div>

                        <div class="bg-emerald-50/60 rounded-xl p-3 border border-emerald-100">
                            <span class="font-bold text-emerald-900 block mb-1 flex items-center gap-1">
                                <i data-lucide="check-circle-2" class="w-3.5 h-3.5 text-emerald-600"></i> Human Ground Truth
                            </span>
                            <p><span class="text-slate-500">Product:</span> <strong class="text-slate-800">${{escapeHtml(item.expected.product)}}</strong></p>
                            <p><span class="text-slate-500">Matter:</span> <strong class="text-slate-800">${{escapeHtml(item.expected.matter)}}</strong></p>
                        </div>
                    </div>
                `;
                container.appendChild(card);
            }});
        }}

        function renderNeedsReview(complaints, threshold) {{
            const reviewItems = complaints.filter(c => c.routing_status === 'Needs Review');
            const container = document.getElementById('review-container');
            document.getElementById('review-badge-count').textContent = reviewItems.length;

            container.innerHTML = '';

            if (reviewItems.length === 0) {{
                container.innerHTML = `
                    <div class="bg-white rounded-xl p-8 text-center text-slate-500 border border-slate-200">
                        <i data-lucide="check-circle" class="w-8 h-8 text-emerald-500 mx-auto mb-2"></i>
                        <p class="font-medium text-sm">Review queue is empty. All complaints met auto-approval threshold.</p>
                    </div>
                `;
                return;
            }}

            reviewItems.forEach(item => {{
                const card = document.createElement('div');
                card.className = 'bg-white rounded-2xl border border-amber-200/80 shadow-sm p-5 hover:shadow-md transition-shadow';
                card.innerHTML = `
                    <div class="flex items-center justify-between border-b border-slate-100 pb-3 mb-3">
                        <div class="flex items-center gap-2">
                            <span class="text-xs font-mono bg-amber-100 text-amber-900 font-bold px-2 py-0.5 rounded">ID #${{item.complaint_id}}</span>
                            <span class="text-xs text-amber-700 font-medium">Below Threshold (${{Math.round(item.predicted.confidence * 100)}}% < ${{Math.round(threshold * 100)}}%)</span>
                        </div>
                        <button onclick="openModalById('${{item.complaint_id}}')" class="text-xs font-semibold text-brand-600 hover:text-brand-700 flex items-center gap-1">
                            Inspect Case <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
                        </button>
                    </div>

                    <div class="mb-4">
                        <p class="text-xs text-slate-800 bg-slate-50 p-3 rounded-xl border border-slate-100 leading-relaxed">
                            ${{escapeHtml(item.complaint_text)}}
                        </p>
                    </div>

                    <div class="flex flex-wrap items-center justify-between gap-3 text-xs bg-amber-50/40 p-3 rounded-xl border border-amber-100">
                        <div>
                            <span class="text-slate-500">Predicted Category:</span>
                            <span class="font-semibold text-slate-900 ml-1">${{escapeHtml(item.predicted.product)}} → ${{escapeHtml(item.predicted.matter)}}</span>
                        </div>
                        <div>
                            <span class="text-slate-500">Evaluation:</span>
                            <span class="font-semibold ${{item.evaluation.classification_correct ? 'text-emerald-700' : 'text-red-600'}} ml-1">
                                ${{item.evaluation.classification_correct ? 'Correct' : 'Incorrect Prediction'}}
                            </span>
                        </div>
                    </div>
                `;
                container.appendChild(card);
            }});
        }}

        function switchTab(tabKey) {{
            document.querySelectorAll('.tab-btn').forEach(btn => {{
                btn.classList.remove('border-brand-500', 'text-brand-600');
                btn.classList.add('border-transparent', 'text-slate-500');
            }});
            document.querySelectorAll('.tab-content').forEach(content => {{
                content.classList.add('hidden');
            }});

            document.getElementById(`tab-${{tabKey}}`).classList.add('border-brand-500', 'text-brand-600');
            document.getElementById(`tab-${{tabKey}}`).classList.remove('border-transparent', 'text-slate-500');
            document.getElementById(`view-${{tabKey}}`).classList.remove('hidden');
        }}

        function openModal(item) {{
            document.getElementById('modal-id').textContent = `#${{item.complaint_id}}`;
            document.getElementById('modal-text').textContent = item.complaint_text;
            
            document.getElementById('modal-pred-product').textContent = item.predicted.product;
            document.getElementById('modal-pred-matter').textContent = item.predicted.matter;
            document.getElementById('modal-pred-conf').textContent = Math.round(item.predicted.confidence * 100) + '%';

            document.getElementById('modal-truth-product').textContent = item.expected.product;
            document.getElementById('modal-truth-matter').textContent = item.expected.matter;

            const isCorrect = item.evaluation.classification_correct;
            document.getElementById('modal-eval-status').innerHTML = `
                <span class="inline-flex items-center gap-1 font-semibold ${{isCorrect ? 'text-emerald-600' : 'text-red-600'}}">
                    <i data-lucide="${{isCorrect ? 'check-circle' : 'x-circle'}}" class="w-3.5 h-3.5"></i>
                    ${{isCorrect ? 'Match' : 'Mismatch'}}
                </span>
            `;

            const isApproved = item.routing_status === 'Approved';
            document.getElementById('modal-routing-badge').innerHTML = `
                <span class="px-2.5 py-1 rounded-full text-xs font-semibold ${{isApproved ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'}}">
                    ${{item.routing_status}}
                </span>
            `;

            document.getElementById('complaint-modal').classList.remove('hidden');
            lucide.createIcons();
        }}

        function openModalById(id) {{
            if (!dashboardData) return;
            const item = dashboardData.complaints.find(c => c.complaint_id === id);
            if (item) openModal(item);
        }}

        function closeModal() {{
            document.getElementById('complaint-modal').classList.add('hidden');
        }}

        function escapeHtml(str) {{
            if (!str) return '';
            return str
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
        }}
    </script>
</body>
</html>
"""

    # 3. Save to 'dashboard/dashboard.html'
    output_dir = "dashboard"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "dashboard.html")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✓ Output successfully generated at: '{output_file}'")
    print("  -> You can now double-click 'dashboard/dashboard.html' to inspect all 50 complaints!")

if __name__ == "__main__":
    main()