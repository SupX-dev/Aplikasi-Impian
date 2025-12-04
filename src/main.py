<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistem Manajemen Inventaris</title>
    <!-- Load Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Load Lucide Icons (as requested by user for modern icons) -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <!-- Load Chart.js for graphs on Dashboard -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        /* Mengatur font Poppins sebagai pengganti font default */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        body {
            font-family: 'Poppins', sans-serif;
            background-color: #f9fafb; /* Putih bersih */
        }
        /* Style untuk sidebar dan main content */
        .sidebar {
            width: 250px;
            background-color: #1e3a8a; /* Biru tua - blue-900 */
            color: white;
            transition: transform 0.3s ease-in-out;
            z-index: 100;
        }
        .sidebar a {
            padding: 1rem 1.5rem;
            display: flex;
            align-items: center;
            border-radius: 0.5rem;
            margin: 0.5rem;
            transition: background-color 0.2s;
        }
        .sidebar a.active {
            background-color: #2563eb; /* blue-600 */
            font-weight: 600;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
        }
        .sidebar a:hover:not(.active) {
            background-color: #172554; /* blue-950 slightly darker on hover */
        }
        .main-content {
            transition: margin-left 0.3s ease-in-out;
            padding-top: 64px; /* Space for the fixed navbar */
        }

        /* Styling for the modal/popup */
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }
        .modal-content {
            background-color: white;
            padding: 2rem;
            border-radius: 1rem;
            width: 90%;
            max-width: 600px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        }

        /* Custom scrollbar for better aesthetics */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-thumb {
            background-color: #94a3b8; /* slate-400 */
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background-color: #64748b; /* slate-500 */
        }

    </style>
</head>
<body class="min-h-screen">

    <!-- 1. Halaman Login (Tampilan default) -->
    <div id="login-view" class="flex justify-center items-center min-h-screen p-4 bg-gray-100">
        <div class="w-full max-w-md bg-white p-8 md:p-10 rounded-xl shadow-2xl transition duration-300">
            <div class="flex flex-col items-center mb-8">
                <i data-lucide="boxes" class="text-blue-600 w-12 h-12 mb-3"></i>
                <h2 class="text-3xl font-bold text-gray-900">Selamat Datang</h2>
                <p class="text-gray-500 mt-1">Sistem Manajemen Inventaris</p>
            </div>

            <form onsubmit="event.preventDefault(); login();">
                <div class="mb-5">
                    <label for="username" class="block text-sm font-medium text-gray-700 mb-2">Nama Pengguna</label>
                    <div class="relative">
                        <i data-lucide="user" class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400"></i>
                        <input type="text" id="username" class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 text-gray-900" placeholder="Masukkan username" required>
                    </div>
                </div>

                <div class="mb-6">
                    <label for="password" class="block text-sm font-medium text-gray-700 mb-2">Kata Sandi</label>
                    <div class="relative">
                        <i data-lucide="lock" class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400"></i>
                        <input type="password" id="password" class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 text-gray-900" placeholder="Masukkan password" required>
                    </div>
                </div>

                <div class="flex items-center justify-between mb-8">
                    <div class="text-sm">
                        <a href="#" class="font-medium text-blue-600 hover:text-blue-800 transition duration-150">Lupa Kata Sandi?</a>
                    </div>
                </div>

                <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-lg transition duration-200 shadow-lg shadow-blue-500/50 transform hover:scale-[1.01]">
                    <i data-lucide="log-in" class="inline w-5 h-5 mr-2"></i>
                    Masuk
                </button>
            </form>
        </div>
    </div>

    <!-- Layout Utama (Muncul setelah login) -->
    <div id="main-layout" class="hidden min-h-screen flex">

        <!-- Sidebar / Menu Samping -->
        <div class="sidebar fixed top-0 left-0 h-screen flex flex-col p-4 shadow-xl">
            <!-- Logo dan Nama Sistem -->
            <div class="p-4 flex items-center mb-6 border-b border-blue-800/50">
                <i data-lucide="boxes" class="w-8 h-8 text-white mr-3"></i>
                <span class="text-xl font-bold">Simanis</span>
            </div>

            <!-- Menu Navigasi -->
            <nav class="flex-grow space-y-2">
                <a href="#" class="nav-link active" data-page="dashboard">
                    <i data-lucide="layout-dashboard" class="w-5 h-5 mr-3"></i> Dashboard
                </a>
                <a href="#" class="nav-link" data-page="barang">
                    <i data-lucide="package" class="w-5 h-5 mr-3"></i> Data Barang
                </a>
                <a href="#" class="nav-link" data-page="transaksi">
                    <i data-lucide="truck" class="w-5 h-5 mr-3"></i> Transaksi
                </a>
                <a href="#" class="nav-link" data-page="laporan">
                    <i data-lucide="bar-chart-2" class="w-5 h-5 mr-3"></i> Laporan
                </a>
                <a href="#" class="nav-link" data-page="pengaturan">
                    <i data-lucide="settings" class="w-5 h-5 mr-3"></i> Pengaturan
                </a>
            </nav>

            <!-- Logout Button -->
            <div class="mt-auto pt-4 border-t border-blue-800/50">
                 <a href="#" onclick="logout();" class="text-red-300 hover:bg-red-900/50 rounded-lg transition duration-200">
                    <i data-lucide="log-out" class="w-5 h-5 mr-3"></i> Keluar
                </a>
            </div>
        </div>

        <!-- Konten Utama -->
        <div class="main-content flex-grow ml-[250px] p-4 sm:p-8">

            <!-- Navbar (Top Header) - Disesuaikan agar lebih mirip gambar -->
            <header class="fixed top-0 right-0 left-[250px] h-16 bg-white shadow-md flex items-center justify-end px-8 z-50">
                <div class="flex items-center space-x-4">
                    <!-- Ikon Pengguna -->
                    <i data-lucide="user-circle" class="w-6 h-6 text-blue-600"></i>
                    <!-- Nama Pengguna Disesuaikan -->
                    <div class="text-sm font-medium text-gray-800">Kurnia Lintang Himayanta</div>
                    <!-- Tombol Logout terpisah -->
                    <a href="#" onclick="logout();" class="text-sm font-medium text-gray-500 hover:text-red-600 transition duration-150">Logout</a>
                </div>
            </header>

            <div id="content-area">
                <!-- 2. Dashboard Utama - Disesuaikan agar lebih mirip gambar -->
                <div id="dashboard-view" class="page-content">
                    <!-- Judul Disesuaikan -->
                    <h1 class="text-3xl font-bold text-gray-900 mb-8 mt-4">Manajemen Inventaris Barang</h1>

                    <!-- Kartu Ringkasan Disesuaikan -->
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                        
                        <!-- Total Barang (150) -->
                        <div class="bg-white p-6 rounded-xl shadow-lg border-t-4 border-blue-600">
                            <div class="flex items-center">
                                <i data-lucide="boxes" class="text-blue-600 w-8 h-8 mr-4"></i>
                                <div>
                                    <p class="text-sm font-medium text-gray-500 uppercase">Total Barang</p>
                                    <p class="text-3xl font-bold text-gray-900">150</p>
                                </div>
                            </div>
                        </div>

                        <!-- Barang Masuk (75) -->
                        <div class="bg-white p-6 rounded-xl shadow-lg border-t-4 border-green-600">
                            <div class="flex items-center">
                                <i data-lucide="download" class="text-green-600 w-8 h-8 mr-4"></i>
                                <div>
                                    <p class="text-sm font-medium text-gray-500 uppercase">Barang Masuk</p>
                                    <p class="text-3xl font-bold text-gray-900">75</p>
                                </div>
                            </div>
                        </div>

                        <!-- Barang Keluar (50) -->
                        <div class="bg-white p-6 rounded-xl shadow-lg border-t-4 border-red-600">
                            <div class="flex items-center">
                                <i data-lucide="upload" class="text-red-600 w-8 h-8 mr-4"></i>
                                <div>
                                    <p class="text-sm font-medium text-gray-500 uppercase">Barang Keluar</p>
                                    <p class="text-3xl font-bold text-gray-900">50</p>
                                </div>
                            </div>
                        </div>

                        <!-- Stok Menipis (5) -->
                        <div class="bg-white p-6 rounded-xl shadow-lg border-t-4 border-yellow-600">
                            <div class="flex items-center">
                                <i data-lucide="alert-triangle" class="text-yellow-600 w-8 h-8 mr-4"></i>
                                <div>
                                    <p class="text-sm font-medium text-gray-500 uppercase">Stok Menipis</p>
                                    <p class="text-3xl font-bold text-gray-900">5</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Grafik dan Riwayat Aktivitas -->
                    <div class="grid grid-cols-1 gap-6">
                        <!-- Grafik Status Stok -->
                        <div class="bg-white p-6 rounded-xl shadow-lg">
                            <h3 class="text-xl font-semibold mb-4 text-gray-800">Status Stok</h3>
                            <canvas id="stockChart" class="h-96"></canvas>
                        </div>

                        <!-- Riwayat Aktivitas Terakhir -->
                        <div class="bg-white p-6 rounded-xl shadow-lg">
                            <h3 class="text-xl font-semibold mb-4 text-gray-800">Riwayat Aktivitas Terakhir</h3>
                            <div class="overflow-x-auto">
                                <table class="min-w-full divide-y divide-gray-200">
                                    <thead class="bg-gray-50">
                                        <tr>
                                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tanggal</th>
                                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Aksi</th>
                                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Barang</th>
                                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Jumlah</th>
                                        </tr>
                                    </thead>
                                    <tbody class="bg-white divide-y divide-gray-200">
                                        <!-- Dummy Data Disesuaikan agar lebih simpel seperti di gambar -->
                                        <tr class="hover:bg-gray-50">
                                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">24 Juni 2024</td>
                                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">Menambahkan</td>
                                            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600">Printer</td>
                                            <td class="px-6 py-4 whitespace-nowrap text-sm text-green-600 font-medium">3</td>
                                        </tr>
                                        <tr class="hover:bg-gray-50">
                                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">22 Juni 2024</td>
                                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">Mengurangi</td>
                                            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600">Laptop Dell</td>
                                            <td class="px-6 py-4 whitespace-nowrap text-sm text-red-600 font-medium">1</td>
                                        </tr>
                                        <tr class="hover:bg-gray-50">
                                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">20 Juni 2024</td>
                                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600">Menambahkan</td>
                                            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600">Kertas A4</td>
                                            <td class="px-6 py-4 whitespace-nowrap text-sm text-green-600 font-medium">50</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 3. Halaman Data Barang -->
                <div id="barang-view" class="page-content hidden">
                    <div class="bg-white p-6 rounded-xl shadow-lg">
                        <div class="flex justify-between items-center mb-6">
                            <h2 class="text-xl font-semibold text-gray-800">Daftar Barang Inventaris</h2>
                            <button onclick="openModal('barang')" class="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg flex items-center transition duration-200 shadow-md">
                                <i data-lucide="plus" class="w-5 h-5 mr-2"></i> Tambah Barang
                            </button>
                        </div>
                        
                        <div class="overflow-x-auto">
                            <table class="min-w-full divide-y divide-gray-200">
                                <thead class="bg-gray-50">
                                    <tr>
                                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nama Barang</th>
                                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Stok</th>
                                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Harga Beli (Rp)</th>
                                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Lokasi</th>
                                        <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Aksi</th>
                                    </tr>
                                </thead>
                                <tbody class="bg-white divide-y divide-gray-200">
                                    <!-- Dummy Data -->
                                    <tr class="hover:bg-gray-50">
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">BRG001</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600">Laptop Dell XPS 13</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900"><span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">120</span></td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">15.000.000</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">Gudang A, Rak 1</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                            <button onclick="openModal('barang', 'edit')" class="text-blue-600 hover:text-blue-900 mr-2"><i data-lucide="edit" class="w-4 h-4 inline"></i></button>
                                            <button class="text-red-600 hover:text-red-900"><i data-lucide="trash-2" class="w-4 h-4 inline"></i></button>
                                        </td>
                                    </tr>
                                     <tr class="hover:bg-gray-50">
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">BRG002</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600">Monitor Samsung 27"</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900"><span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800">15</span></td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">2.500.000</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">Gudang B, Rak 3</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                            <button onclick="openModal('barang', 'edit')" class="text-blue-600 hover:text-blue-900 mr-2"><i data-lucide="edit" class="w-4 h-4 inline"></i></button>
                                            <button class="text-red-600 hover:text-red-900"><i data-lucide="trash-2" class="w-4 h-4 inline"></i></button>
                                        </td>
                                    </tr>
                                     <tr class="hover:bg-gray-50">
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">BRG003</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600">Kertas A4 Sinar Dunia</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900"><span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800">5</span></td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">50.000</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">Ruang Arsip, Rak 5</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                            <button onclick="openModal('barang', 'edit')" class="text-blue-600 hover:text-blue-900 mr-2"><i data-lucide="edit" class="w-4 h-4 inline"></i></button>
                                            <button class="text-red-600 hover:text-red-900"><i data-lucide="trash-2" class="w-4 h-4 inline"></i></button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- 4. Halaman Transaksi -->
                <div id="transaksi-view" class="page-content hidden">
                    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                        <!-- Form Transaksi -->
                        <div class="lg:col-span-1 bg-white p-6 rounded-xl shadow-lg h-fit">
                            <h2 class="text-xl font-semibold mb-6 text-gray-800">Input Transaksi Baru</h2>
                            <form onsubmit="event.preventDefault(); alert('Transaksi Tersimpan!');">
                                <div class="mb-5">
                                    <label class="block text-sm font-medium text-gray-700 mb-2">Jenis Transaksi</label>
                                    <select class="w-full border border-gray-300 rounded-lg p-2.5 focus:ring-blue-500 focus:border-blue-500 text-gray-900">
                                        <option>Barang Masuk</option>
                                        <option>Barang Keluar</option>
                                    </select>
                                </div>
                                <div class="mb-5">
                                    <label class="block text-sm font-medium text-gray-700 mb-2">Tanggal</label>
                                    <input type="date" value="2025-10-07" class="w-full border border-gray-300 rounded-lg p-2.5 focus:ring-blue-500 focus:border-blue-500 text-gray-900" required>
                                </div>
                                <div class="mb-5">
                                    <label class="block text-sm font-medium text-gray-700 mb-2">Nama Barang</label>
                                    <select class="w-full border border-gray-300 rounded-lg p-2.5 focus:ring-blue-500 focus:border-blue-500 text-gray-900" required>
                                        <option>Laptop Dell XPS 13</option>
                                        <option>Monitor Samsung 27"</option>
                                        <option>Kertas A4 Sinar Dunia</option>
                                    </select>
                                </div>
                                <div class="mb-5">
                                    <label class="block text-sm font-medium text-gray-700 mb-2">Jumlah Unit</label>
                                    <input type="number" min="1" value="1" class="w-full border border-gray-300 rounded-lg p-2.5 focus:ring-blue-500 focus:border-blue-500 text-gray-900" required>
                                </div>
                                <div class="mb-6">
                                    <label class="block text-sm font-medium text-gray-700 mb-2">Keterangan</label>
                                    <textarea rows="3" class="w-full border border-gray-300 rounded-lg p-2.5 focus:ring-blue-500 focus:border-blue-500 text-gray-900" placeholder="Contoh: Pembelian dari Supplier X atau Pengiriman ke Divisi Marketing"></textarea>
                                </div>
                                <button type="submit" class="w-full bg-green-600 hover:bg-green-700 text-white font-medium py-3 rounded-lg flex items-center justify-center transition duration-200 shadow-md">
                                    <i data-lucide="save" class="w-5 h-5 mr-2"></i> Simpan Transaksi
                                </button>
                            </form>
                        </div>

                        <!-- Riwayat Transaksi -->
                        <div class="lg:col-span-2 bg-white p-6 rounded-xl shadow-lg">
                            <h2 class="text-xl font-semibold mb-4 text-gray-800">Riwayat Transaksi</h2>
                             <div class="overflow-x-auto">
                                <table class="min-w-full divide-y divide-gray-200">
                                    <thead class="bg-gray-50">
                                        <tr>
                                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tanggal</th>
                                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Jenis</th>
                                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Barang</th>
                                            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Jumlah</th>
                                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Keterangan</th>
                                        </tr>
                                    </thead>
                                    <tbody class="bg-white divide-y divide-gray-200">
                                        <!-- Dummy Data -->
                                        <tr class="hover:bg-gray-50">
                                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">05/10/2025</td>
                                            <td class="px-6 py-4 whitespace-nowrap text-sm"><span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">MASUK</span></td>
                                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">Laptop Dell XPS 13</td>
                                            <td class="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-900">+50</td>
                                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">Pembelian batch Q4</td>
                                        </tr>
                                         <tr class="hover:bg-gray-50">
                                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">03/10/2025</td>
                                            <td class="px-6 py-4 whitespace-nowrap text-sm"><span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800">KELUAR</span></td>
                                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">Monitor Samsung 27"</td>
                                            <td class="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-900">-15</td>
                                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">Pengadaan Divisi Keuangan</td>
                                        </tr>
                                        <tr class="hover:bg-gray-50">
                                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">01/10/2025</td>
                                            <td class="px-6 py-4 whitespace-nowrap text-sm"><span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">MASUK</span></td>
                                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">Kertas A4 Sinar Dunia</td>
                                            <td class="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-900">+500</td>
                                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">Stok rutin bulanan</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 5. Halaman Laporan -->
                <div id="laporan-view" class="page-content hidden">
                    <div class="bg-white p-6 rounded-xl shadow-lg">
                        <h2 class="text-xl font-semibold mb-4 text-gray-800">Laporan Inventaris</h2>

                        <!-- Filter dan Tombol Aksi -->
                        <div class="flex flex-col sm:flex-row gap-4 mb-6 p-4 bg-gray-50 rounded-lg border">
                            <div class="flex-grow">
                                <label for="filter-start" class="block text-sm font-medium text-gray-700 mb-1">Dari Tanggal</label>
                                <input type="date" id="filter-start" value="2025-09-01" class="w-full border border-gray-300 rounded-lg p-2.5 text-gray-900">
                            </div>
                            <div class="flex-grow">
                                <label for="filter-end" class="block text-sm font-medium text-gray-700 mb-1">Sampai Tanggal</label>
                                <input type="date" id="filter-end" value="2025-10-07" class="w-full border border-gray-300 rounded-lg p-2.5 text-gray-900">
                            </div>
                            <div class="flex items-end space-x-2 pt-2 sm:pt-0">
                                <button class="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5 px-4 rounded-lg flex items-center transition duration-200">
                                    <i data-lucide="filter" class="w-5 h-5 mr-2"></i> Tampilkan
                                </button>
                                <button onclick="alert('Mencetak Laporan ke PDF...')" class="bg-red-600 hover:bg-red-700 text-white font-medium py-2.5 px-4 rounded-lg flex items-center transition duration-200">
                                    <i data-lucide="file-text" class="w-5 h-5 mr-2"></i> Cetak PDF
                                </button>
                                <button onclick="alert('Mengekspor Laporan ke Excel...')" class="bg-green-600 hover:bg-green-700 text-white font-medium py-2.5 px-4 rounded-lg flex items-center transition duration-200">
                                    <i data-lucide="sheet" class="w-5 h-5 mr-2"></i> Ekspor Excel
                                </button>
                            </div>
                        </div>

                        <!-- Tabel Hasil Laporan -->
                        <div class="overflow-x-auto">
                            <table class="min-w-full divide-y divide-gray-200 border border-gray-100">
                                <thead class="bg-blue-900 text-white">
                                    <tr>
                                        <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Barang ID</th>
                                        <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Nama Barang</th>
                                        <th class="px-6 py-3 text-right text-xs font-medium uppercase tracking-wider">Stok Awal</th>
                                        <th class="px-6 py-3 text-right text-xs font-medium uppercase tracking-wider">Total Masuk</th>
                                        <th class="px-6 py-3 text-right text-xs font-medium uppercase tracking-wider">Total Keluar</th>
                                        <th class="px-6 py-3 text-right text-xs font-medium uppercase tracking-wider">Stok Akhir</th>
                                    </tr>
                                </thead>
                                <tbody class="bg-white divide-y divide-gray-200">
                                    <!-- Dummy Data -->
                                    <tr class="hover:bg-gray-50">
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">BRG001</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600">Laptop Dell XPS 13</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-700">70</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-right text-sm text-green-600 font-medium">+50</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-right text-sm text-red-600 font-medium">-0</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-bold text-gray-900">120</td>
                                    </tr>
                                     <tr class="hover:bg-gray-50">
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">BRG002</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600">Monitor Samsung 27"</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-700">30</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-right text-sm text-green-600 font-medium">+0</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-right text-sm text-red-600 font-medium">-15</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-bold text-gray-900">15</td>
                                    </tr>
                                     <tr class="hover:bg-gray-50">
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">BRG003</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600">Kertas A4 Sinar Dunia</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900"><span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800">5</span></td>
                                        <td class="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-700">5</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-right text-sm text-green-600 font-medium">+500</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-right text-sm text-red-600 font-medium">-500</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-bold text-gray-900">5</td>
                                    </tr>
                                    <tr class="bg-gray-100 font-bold">
                                        <td colspan="5" class="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-900">Total Stok Akhir:</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-right text-sm text-blue-700">140</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- 6. Halaman Pengaturan Akun -->
                <div id="pengaturan-view" class="page-content hidden">
                    <div class="bg-white p-8 rounded-xl shadow-lg w-full max-w-2xl mx-auto">
                        <h2 class="text-2xl font-semibold mb-6 text-gray-800 border-b pb-3">Pengaturan Profil Pengguna</h2>
                        <form onsubmit="event.preventDefault(); alert('Perubahan profil tersimpan!');">
                            <!-- Ubah Nama -->
                            <div class="mb-5">
                                <label for="setting-name" class="block text-sm font-medium text-gray-700 mb-2">Nama Lengkap</label>
                                <input type="text" id="setting-name" value="Admin Utama" class="w-full border border-gray-300 rounded-lg p-3 focus:ring-blue-500 focus:border-blue-500 text-gray-900" required>
                            </div>

                            <!-- Ubah Email -->
                            <div class="mb-5">
                                <label for="setting-email" class="block text-sm font-medium text-gray-700 mb-2">Alamat Email</label>
                                <input type="email" id="setting-email" value="admin.utama@simanis.com" class="w-full border border-gray-300 rounded-lg p-3 focus:ring-blue-500 focus:border-blue-500 text-gray-900" required>
                            </div>

                            <!-- Ubah Password -->
                            <div class="mb-6 border-t pt-4 mt-4">
                                <h3 class="text-lg font-medium text-gray-800 mb-4">Ubah Kata Sandi</h3>
                                <div class="mb-4">
                                    <label for="setting-old-password" class="block text-sm font-medium text-gray-700 mb-2">Kata Sandi Lama</label>
                                    <input type="password" id="setting-old-password" class="w-full border border-gray-300 rounded-lg p-3 focus:ring-blue-500 focus:border-blue-500 text-gray-900" placeholder="Masukkan kata sandi lama">
                                </div>
                                <div class="mb-4">
                                    <label for="setting-new-password" class="block text-sm font-medium text-gray-700 mb-2">Kata Sandi Baru</label>
                                    <input type="password" id="setting-new-password" class="w-full border border-gray-300 rounded-lg p-3 focus:ring-blue-500 focus:border-blue-500 text-gray-900" placeholder="Masukkan kata sandi baru">
                                </div>
                                <div class="mb-4">
                                    <label for="setting-confirm-password" class="block text-sm font-medium text-gray-700 mb-2">Konfirmasi Kata Sandi Baru</label>
                                    <input type="password" id="setting-confirm-password" class="w-full border border-gray-300 rounded-lg p-3 focus:ring-blue-500 focus:border-blue-500 text-gray-900" placeholder="Ulangi kata sandi baru">
                                </div>
                            </div>

                            <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 rounded-lg flex items-center justify-center transition duration-200 shadow-lg mt-6">
                                <i data-lucide="save" class="w-5 h-5 mr-2"></i> Simpan Perubahan
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Modal for Add/Edit Barang (Popup Modal) -->
    <div id="modal-barang" class="modal-overlay">
        <div class="modal-content">
            <div class="flex justify-between items-center border-b pb-3 mb-4">
                <h3 id="modal-title" class="text-xl font-semibold text-gray-800">Tambah Barang Baru</h3>
                <button onclick="closeModal('barang')" class="text-gray-400 hover:text-gray-700 transition"><i data-lucide="x" class="w-6 h-6"></i></button>
            </div>
            <form>
                <div class="mb-4">
                    <label for="barang-nama" class="block text-sm font-medium text-gray-700 mb-2">Nama Barang</label>
                    <input type="text" id="barang-nama" class="w-full border border-gray-300 rounded-lg p-2.5 text-gray-900" placeholder="Contoh: Meja Ergonomis Tipe C" required>
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div class="mb-4">
                        <label for="barang-stok" class="block text-sm font-medium text-gray-700 mb-2">Stok Awal</label>
                        <input type="number" id="barang-stok" min="0" value="0" class="w-full border border-gray-300 rounded-lg p-2.5 text-gray-900" required>
                    </div>
                    <div class="mb-4">
                        <label for="barang-harga" class="block text-sm font-medium text-gray-700 mb-2">Harga Beli (Rp)</label>
                        <input type="number" id="barang-harga" min="0" value="0" class="w-full border border-gray-300 rounded-lg p-2.5 text-gray-900" required>
                    </div>
                </div>
                <div class="mb-4">
                    <label for="barang-lokasi" class="block text-sm font-medium text-gray-700 mb-2">Lokasi Penyimpanan</label>
                    <input type="text" id="barang-lokasi" class="w-full border border-gray-300 rounded-lg p-2.5 text-gray-900" placeholder="Contoh: Gudang C, Rak 2">
                </div>
                <div class="flex justify-end pt-4">
                    <button type="button" onclick="closeModal('barang')" class="bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-2 px-4 rounded-lg mr-2 transition duration-200">Batal</button>
                    <button type="submit" class="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg flex items-center transition duration-200">
                        <i data-lucide="save" class="w-5 h-5 mr-2"></i> Simpan Barang
                    </button>
                </div>
            </form>
        </div>
    </div>

    <!-- JavaScript untuk Navigasi dan Chart -->
    <script>
        const loginView = document.getElementById('login-view');
        const mainLayout = document.getElementById('main-layout');
        const contentArea = document.getElementById('content-area');
        const navLinks = document.querySelectorAll('.nav-link');
        // pageTitle tidak lagi digunakan untuk Dashboard
        let chartInstance = null;

        // Fungsi untuk mengautentikasi (simulasi)
        function login() {
            // Dalam aplikasi nyata, lakukan validasi kredensial di sini
            console.log('Login attempt...');
            loginView.classList.add('hidden');
            mainLayout.classList.remove('hidden');
            navigateTo('dashboard');
            // Re-render Lucide icons for the main layout
            lucide.createIcons();
        }

        // Fungsi untuk logout (simulasi)
        function logout() {
            // Mengganti alert dengan struktur yang aman (meskipun ini hanya simulasi)
            if (confirmLogout()) {
                console.log('Logout success.');
                mainLayout.classList.add('hidden');
                loginView.classList.remove('hidden');
            }
        }
        
        // Pengganti window.confirm() untuk logout
        function confirmLogout() {
             // Karena window.confirm() tidak disarankan, ini adalah simulasi sederhana.
            // Dalam UI nyata, ini harus diganti dengan modal konfirmasi.
            return true; 
        }

        // Fungsi untuk navigasi antar halaman
        function navigateTo(pageId) {
            // 1. Sembunyikan semua konten halaman
            document.querySelectorAll('.page-content').forEach(view => {
                view.classList.add('hidden');
            });

            // 2. Tampilkan halaman yang diminta
            const targetView = document.getElementById(`${pageId}-view`);
            if (targetView) {
                targetView.classList.remove('hidden');
            }

            // 3. Perbarui Judul Halaman di Navbar
            // Judul di Navbar hanya diubah jika BUKAN Dashboard
            const mainHeader = document.querySelector('.main-content > header');
            const pageTitleInContent = document.querySelector('#dashboard-view h1');

            if (pageId === 'dashboard') {
                // Sembunyikan header top (kecuali user info) jika di Dashboard, karena judul utama ada di body
                mainHeader.classList.add('justify-end'); // Geser user info ke kanan
                if (pageTitleInContent) pageTitleInContent.classList.remove('hidden');
            } else {
                 // Tampilkan header top dan atur judul
                mainHeader.classList.remove('justify-end');
                // Ganti judul di header top (untuk halaman selain dashboard)
                const headerTitle = document.getElementById('page-title');
                if (headerTitle) {
                    let title = '';
                    switch (pageId) {
                        case 'barang': title = 'Data Barang'; break;
                        case 'transaksi': title = 'Transaksi Inventaris'; break;
                        case 'laporan': title = 'Laporan & Analisis'; break;
                        case 'pengaturan': title = 'Pengaturan Akun'; break;
                        default: title = 'Sistem Inventaris'; break;
                    }
                    headerTitle.textContent = title;
                    headerTitle.classList.remove('hidden'); // Pastikan judul muncul
                }
            }


            // 4. Perbarui status aktif di Sidebar
            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('data-page') === pageId) {
                    link.classList.add('active');
                }
            });

            // 5. Inisialisasi Chart jika di Dashboard
            if (pageId === 'dashboard') {
                initializeChart();
            } else {
                // Hapus chart agar tidak error saat berpindah
                if (chartInstance) {
                    chartInstance.destroy();
                    chartInstance = null;
                }
            }
        }

        // Event listener untuk menu navigasi
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const pageId = e.currentTarget.getAttribute('data-page');
                navigateTo(pageId);
            });
        });

        // Fungsi untuk inisialisasi Chart.js
        function initializeChart() {
            if (chartInstance) {
                chartInstance.destroy(); // Hapus instance lama jika ada
            }

            const ctx = document.getElementById('stockChart').getContext('2d');
            
            // Data Dummy BAR CHART: Menampilkan Total Stok berdasarkan Kategori Barang (contoh: Elektronik, Alat Tulis, Furnitur)
            const data = {
                labels: ['Elektronik', 'Alat Tulis', 'Furnitur', 'Perkakas'], 
                datasets: [{
                    label: 'Total Stok Saat Ini (Unit)',
                    data: [80, 250, 45, 120], 
                    backgroundColor: [
                        'rgba(37, 99, 235, 0.8)', // Biru untuk Elektronik
                        'rgba(22, 163, 74, 0.8)', // Hijau untuk Alat Tulis
                        'rgba(234, 179, 8, 0.8)', // Kuning untuk Furnitur
                        'rgba(239, 68, 68, 0.8)' // Merah untuk Perkakas
                    ],
                    borderColor: [
                        'rgba(37, 99, 235, 1)', 
                        'rgba(22, 163, 74, 1)', 
                        'rgba(234, 179, 8, 1)',
                        'rgba(239, 68, 68, 1)'
                    ],
                    borderWidth: 1,
                    borderRadius: 8, // Tambahkan sudut membulat pada bar
                }]
            };

            const config = {
                type: 'bar', // Menggunakan BAR Chart
                data: data,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Jumlah Unit (Total Stok)'
                            }
                        },
                         x: {
                            grid: {
                                display: false 
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false // Sembunyikan legend karena hanya ada 1 dataset
                        },
                        title: {
                            display: false,
                        }
                    }
                }
            };

            chartInstance = new Chart(ctx, config);
        }

        // Fungsi untuk membuka modal
        function openModal(modalType, action = 'add') {
            if (modalType === 'barang') {
                const modal = document.getElementById('modal-barang');
                const title = document.getElementById('modal-title');
                if (action === 'edit') {
                    title.textContent = 'Edit Data Barang (BRG001)';
                } else {
                    title.textContent = 'Tambah Barang Baru';
                }
                modal.style.display = 'flex';
            }
        }

        // Fungsi untuk menutup modal
        function closeModal(modalType) {
             if (modalType === 'barang') {
                document.getElementById('modal-barang').style.display = 'none';
            }
        }

        // Inisialisasi: Render semua ikon Lucide pada saat load awal
        window.onload = function() {
            lucide.createIcons();
        };

    </script>
</body>
</html>
