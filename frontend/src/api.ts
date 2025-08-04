export const fetchProducts = async (categorySlug: string) => {
  const response = await fetch(`http://127.0.0.1:8000/api/products/products/?category_slug=${categorySlug}`);
  return response.json();
};

export const fetchSalesChart = async () => {
  const response = await fetch('http://127.0.0.1:8000/api/products/sales-chart/');
  return response.json();
};

export const uploadImage = async (productId: number, file: File) => {
  const formData = new FormData();
  formData.append('image', file);
  const token = localStorage.getItem('token'); // فرض می‌کنیم توکن تو localStorage ذخیره شده
  const response = await fetch(`http://127.0.0.1:8000/api/products/${productId}/images/`, {
    method: 'POST',
    headers: token ? { Authorization: `Bearer ${token}` } : {},
    body: formData,
  });
  return response.json();
};