import { Routes, Route, useNavigate } from "react-router-dom";
import Home from "./pages/Home";
import Image from "./pages/Image";
import { useState, useEffect } from "react";
import { TOKEN_STORAGE_KEY, API_URL } from "./lib/constants";
import { User, Toast } from "./lib/types";
import { Button } from "./components/ui/button";
import { AppContext } from "./hooks/context";
import { fetchTokenFromAPI, fetchUserFromAPI } from "./lib/api";
import {
  ExclamationTriangleIcon,
  CheckIcon,
  PersonIcon,
} from "@radix-ui/react-icons";
import { Alert, AlertTitle, AlertDescription } from "./components/ui/alert";
import { Input } from "./components/ui/input";
import { Label } from "./components/ui/label";

const EMPTY_LOGIN_FORM = { username: "", password: "" };

const App = () => {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState(EMPTY_LOGIN_FORM);
  const [user, setUser] = useState<User | undefined>();
  const [toast, setToast] = useState<Toast | undefined>();

  useEffect(() => {
    const fetchUser = async () => {
      const token = localStorage.getItem(TOKEN_STORAGE_KEY);
      if (token) {
        setLoading(true);
        const { data, error } = await fetchUserFromAPI(token);
        setLoading(false);

        if (error) {
          localStorage.removeItem(TOKEN_STORAGE_KEY);
          setToast({ type: "error", message: error });
        } else {
          setUser(data);
        }
      }
    };

    fetchUser();
  }, []);

  const handleFormChange =
    (key: string) => (e: React.ChangeEvent<HTMLInputElement>) => {
      setForm((o) => ({ ...o, [key]: e.target.value }));
    };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();

    setLoading(true);
    const { data: token, error: tokenError } = await fetchTokenFromAPI(
      form.username,
      form.password
    );

    if (tokenError) {
      setToast({ type: "error", message: tokenError });
      setLoading(false);
      return;
    }

    setForm(EMPTY_LOGIN_FORM);
    localStorage.setItem(TOKEN_STORAGE_KEY, token.access_token);

    const { data: user, error } = await fetchUserFromAPI(token.access_token);
    setLoading(false);

    if (error) {
      setToast({ message: error, type: "error" });
    } else {
      setUser(user);
    }
  };

  const handleLogout = () => {
    setUser(undefined);
    localStorage.removeItem(TOKEN_STORAGE_KEY);
    navigate("/");
  };

  useEffect(() => {
    if (toast) {
      setTimeout(() => {
        setToast(undefined);
      }, 3000);
    }
  }, [toast]);

  const toastNode = toast && (
    <div className="fixed bottom-5 left-5 bg-background">
      <Alert variant={toast.type === "error" ? "destructive" : "success"}>
        {toast.type === "error" ? (
          <ExclamationTriangleIcon className="h-4 w-4" />
        ) : (
          <CheckIcon className="h-4 w-4" />
        )}
        <AlertTitle>{toast.type === "error" ? "Error" : "Success!"}</AlertTitle>
        <AlertDescription>{toast.message}</AlertDescription>
      </Alert>
    </div>
  );

  const loadingNode = loading && (
    <div className="absolute bottom-5 right-5">Loading...</div>
  );

  if (!user) {
    return (
      <div className="relative flex h-screen w-screen">
        <form
          onSubmit={handleLogin}
          method="post"
          className="w-full flex flex-col gap-2 items-center justify-center p-4"
        >
          <div className="flex items-center gap-2 p-2">
            <img src="/picky.svg" className="h-[40px] lg:h-[50px] w-auto" />
            <h2 className="text-2xl font-bold">Image Compression</h2>
          </div>
          <Label htmlFor="username">Username</Label>
          <Input
            name="username"
            onChange={handleFormChange("username")}
            value={form["username"]}
          />
          <Label htmlFor="password">Password</Label>
          <Input
            name="password"
            onChange={handleFormChange("password")}
            value={form["password"]}
            type="password"
          />
          <Button type="submit">Login</Button>
        </form>
        {toastNode}
        {loadingNode}
      </div>
    );
  }

  return (
    <div className="flex flex-col p-4 relative h-screen w-screen">
      <div className="flex justify-between items-center p-4 bg-accent">
        <div className="flex items-center gap-2 p-2">
          <a href="/">
            <img src="/picky.svg" className="h-[40px] lg:h-[50px] w-auto" />
          </a>
          <h2 className="text-2xl font-bold">Image Compression</h2>
        </div>
        <div>
          <div className="flex gap-1 items-center text-xl">
            <PersonIcon />
            <h2>{user.username}</h2>
          </div>
          <Button onClick={handleLogout}>Logout</Button>
        </div>
      </div>

      <div className="flex justify-center items-center">
        <AppContext.Provider value={{ user, setToast, setLoading }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/image/:imageId" element={<Image />} />
          </Routes>
        </AppContext.Provider>
      </div>
      {toastNode}
      {loadingNode}
    </div>
  );
};

export default App;
