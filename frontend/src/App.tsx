import "./App.css";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "./api/baseQuery";
import withSuspense from "./components/withSuspend";
import { lazy, useEffect, useState } from "react";
import { fetchProducts, fetchSalesChart, uploadImage } from './api';
import { Bar } from 'react-chartjs-2';

const AppRoutes = withSuspense(lazy(() => import("./routes")));

function AppContent() {
  const [products, setProducts] = useState<any[]>([]);
  const [chartData, setChartData] = useState<{ labels: string[]; sales: number[] }>({ labels: [], sales: [] });
  const [file, setFile] = useState<File | null>(null);

  useEffect(() => {
    fetchProducts('smartphones').then(data => setProducts(data));
    fetchSalesChart().then(data => setChartData(data));
  }, []);

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (file && file.type.startsWith('image/')) {
      await uploadImage(2, file); // مثلاً برای product_id=2
      alert('Image uploaded!');
    }
  };

  const chart = {
    labels: chartData.labels,
    datasets: [{ label: 'Sales', data: chartData.sales, backgroundColor: 'rgba(75,192,192,0.4)' }],
  };

  return (
    <div>
      <h1>Products</h1>
      {products.map((product) => (
        <div key={product.id}>
          {product.title} (Sales: {product.store_items[0].sales_count})
        </div>
      ))}
      <h1>Sales Chart</h1>
      <Bar data={chart} />
      <h1>Upload Image</h1>
      <form onSubmit={handleUpload}>
        <input type="file" accept="image/*" onChange={(e) => setFile(e.target.files?.[0] || null)} />
        <button type="submit">Upload</button>
      </form>
      <AppRoutes />
    </div>
  );
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AppContent />
    </QueryClientProvider>
  );
}