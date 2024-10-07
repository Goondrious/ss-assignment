import React from "react";
import { Toast, User } from "@/lib/types";

export const AppContext = React.createContext<{
  user?: User;
  setToast: (t: Toast) => void;
  setLoading: (b: boolean) => void;
}>({
  setToast: () => {},
  setLoading: () => {},
});
