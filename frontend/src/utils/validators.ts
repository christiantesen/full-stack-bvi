// Form validation rules
export const required = (value: any) => !!value || 'Field is required';
export const email = (value: string) => {
  const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return pattern.test(value) || 'Invalid email format';
};

// Add more validators as needed