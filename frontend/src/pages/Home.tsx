import { ChangeEvent, useContext, useEffect, useState } from "react";
import { Button } from "../components/ui/button";
import { useNavigate } from "react-router-dom";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from "../components/ui/card";
import { UserImage } from "@/lib/types";
import { useImages } from "@/hooks/image";
import {
  deleteImageFromAPI,
  fetchImagesFromAPI,
  uploadImageToAPI,
} from "@/lib/api";
import { API_URL, TOKEN_STORAGE_KEY } from "@/lib/constants";
import { AppContext } from "@/hooks/context";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { ExclamationTriangleIcon, TrashIcon } from "@radix-ui/react-icons";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

function App() {
  const navigate = useNavigate();
  const { user, setToast, setLoading } = useContext(AppContext);

  const [file, setFile] = useState<File | undefined>();
  const [fileName, setFileName] = useState<string>("");

  const { images, setImages, addImage, removeImage } = useImages();

  useEffect(() => {
    const fetchImages = async () => {
      const token = localStorage.getItem(TOKEN_STORAGE_KEY);
      if (!token) return;

      setLoading(true);
      const { data, error } = await fetchImagesFromAPI(token);
      setLoading(false);

      if (error) {
        setToast({ type: "error", message: error });
      } else {
        setImages(data);
      }
    };

    if (user) fetchImages();
  }, [user]);

  const handleRemoveImage = (image: UserImage) => async () => {
    const token = localStorage.getItem(TOKEN_STORAGE_KEY);
    if (!token) return;

    setLoading(true);
    const { error } = await deleteImageFromAPI(image.id, token);
    setLoading(false);

    if (error) {
      setToast({ type: "error", message: error });
      return;
    }

    setToast({ type: "success", message: "Image deleted!" });
    removeImage(image);
  };

  const handleSelectImage = (e: ChangeEvent<HTMLInputElement>) => {
    setFile(e.target.files?.[0]);
  };

  const handleFileUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file || !fileName) return;
    const token = localStorage.getItem(TOKEN_STORAGE_KEY);
    if (!token) return;

    setLoading(true);
    const { data, error } = await uploadImageToAPI(file, fileName, token);
    setLoading(false);

    if (error) {
      setToast({ type: "error", message: error });
      return;
    }

    addImage(data.file);
    setToast({ type: "success", message: "Image uploaded!" });
  };

  return (
    <div>
      {Object.keys(images).length < 10 ? (
        <form
          onSubmit={handleFileUpload}
          method="post"
          className="flex flex-col gap-2 mt-2"
        >
          <h2 className="text-xl font-semibold">Upload New Image</h2>
          <Label htmlFor="fileName" className="font-semibold">
            File name
          </Label>
          <Input
            name="fileName"
            value={fileName}
            onChange={(e) => setFileName(e.target.value)}
          />
          <Label htmlFor="img" className="font-semibold">
            Select image
          </Label>
          <Input
            type="file"
            id="img"
            name="img"
            accept="image/*"
            onChange={handleSelectImage}
          />
          {file && (
            <section>
              <h2 className="font-semibold">File details</h2>
              <ul>
                <li>Name: {file.name}</li>
                <li>Type: {file.type}</li>
                <li>Size: {file.size} bytes</li>
              </ul>
            </section>
          )}
          <Button onClick={handleFileUpload} disabled={!file || !fileName}>
            Upload
          </Button>
        </form>
      ) : (
        <Alert variant="default">
          <ExclamationTriangleIcon className="h-4 w-4" />
          <AlertTitle>Image Limit Reached</AlertTitle>
          <AlertDescription>
            You can only have 10 images. Please delete some.
          </AlertDescription>
        </Alert>
      )}
      {Object.keys(images).length > 0 ? (
        <h1 className="text-xl font-semibold mt-4">Your Images</h1>
      ) : (
        <div>You have no images. Upload one to start compressing!</div>
      )}
      <div className="flex gap-2 p-2 flex-wrap">
        {Object.values(images).map((o) => (
          <Card key={o.id}>
            <CardHeader>
              <div className="flex justify-between">
                <div className="flex flex-col gap-1">
                  <CardTitle>{o.name}</CardTitle>
                  <CardDescription>
                    Uploaded on {o.uploaded_at.toLocaleString()}
                  </CardDescription>
                </div>
                <Button
                  variant="link"
                  onClick={() => navigate(`/image/${o.id}`)}
                >
                  View image page
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <img src={`${API_URL}${o.signed_url}`} />
            </CardContent>
            <CardFooter>
              <div className="flex justify-between items-center w-full">
                <div className="text-md font-light">
                  This image has {o.num_compressions} compression
                  {o.num_compressions !== 1 ? "s" : ""}
                </div>

                <Button variant="destructive" onClick={handleRemoveImage(o)}>
                  <TrashIcon />
                </Button>
              </div>
            </CardFooter>
          </Card>
        ))}
      </div>
    </div>
  );
}

export default App;
