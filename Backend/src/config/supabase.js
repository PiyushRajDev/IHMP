import { createClient } from '@supabase/supabase-js';  

const supabaseUrl = 'https://qicdbfueadwfgtvjhfpe.supabase.co'; // Replace with your actual Supabase URL  
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFpY2RiZnVlYWR3Zmd0dmpoZnBlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDExMTAzOTQsImV4cCI6MjA1NjY4NjM5NH0.jD75PlOzStPngIYaX4CrEWOWcYrJK2xkEu6HbAF4NNk'; // Replace with your actual Supabase Anon Key  

const supabase = createClient(supabaseUrl, supabaseAnonKey);  

export default supabase;  