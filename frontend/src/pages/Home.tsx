import { ChangeEvent, useEffect, useState } from "react";
import { Button } from "../components/ui/button";
import { ExclamationTriangleIcon } from "@radix-ui/react-icons";
import { useNavigate } from "react-router-dom";
import { Alert, AlertTitle, AlertDescription } from "../components/ui/alert";
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

const API_URL = "http://localhost:8000";

const uploadFile = async (file: File) => {
  try {
    const formData = new FormData();

    formData.append("file", file);

    formData.append("quality", "1");
    formData.append("resizeWidth", "50");

    const res = await fetch(`${API_URL}/upload-image`, {
      method: "POST",
      body: formData,
    });

    // catch api .error first, then status text as a fallback
    if (!res.ok) {
      const error = await res
        .json()
        .then((o) => o.error)
        .catch((o) => o.text);
      throw new Error(error);
    }

    const data = await res.json();

    if (data.success) {
      return { success: true };
    }

    return { error: data.error };
  } catch (e: any) {
    console.error("API Upload Error = ", e.message);
    return { error: e.message };
  }
};

const NEW_IMAGE = {
  id: `${Math.random()}`,
  userId: "1",
  path: "/elephant test-compressed.jpg",
  name: "Elephant",
  uploadedAt: new Date(),
  numCompressions: 2,
};

const IMAGES: UserImage[] = [
  {
    id: "1",
    userId: "1",
    path: "/elephant test-compressed.jpg",
    name: "Elephant",
    uploadedAt: new Date(),
    numCompressions: 2,
  },
  {
    id: "2",
    userId: "1",
    path: "/link-compressed.png",
    name: "Link",
    uploadedAt: new Date(),
    numCompressions: 3,
  },
];

function App() {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");
  const [file, setFile] = useState<undefined | File>();

  const { images, setImages, addImage, removeImage } = useImages();
  useEffect(() => {
    setImages(IMAGES.reduce((agg, o) => ({ ...agg, [o.id]: o }), {}));
  }, []);

  const handleAddImage = () => {
    addImage(NEW_IMAGE);
  };

  const handleRemoveImage = (image: UserImage) => () => {
    removeImage(image);
  };

  const handleSelectImage = (e: ChangeEvent<HTMLInputElement>) => {
    setFile(e.target.files?.[0]);
    setError("");
    setSuccess(false);
  };

  const handleFileUpload = async () => {
    if (!file) return;
    setError("");
    setSuccess(false);
    setLoading(true);
    const result = await uploadFile(file);
    setLoading(false);
    if (result.success) {
      setSuccess(true);
    } else {
      setError(result.error);
    }
  };

  return (
    <>
      <h1 className="text-xl">Your Images</h1>
      <div>
        <label htmlFor="img">Select image:</label>
        <input
          type="file"
          id="img"
          name="img"
          accept="image/*"
          onChange={handleSelectImage}
          disabled={loading}
        />
        {file && (
          <section>
            File details:
            <ul>
              <li>Name: {file.name}</li>
              <li>Type: {file.type}</li>
              <li>Size: {file.size} bytes</li>
            </ul>
          </section>
        )}
        <Button onClick={handleFileUpload} disabled={!file}>
          Upload new image
        </Button>
        <Button onClick={handleAddImage}>Add Image</Button>
        <p>
          {success && "File successfully uploaded!"}
          {loading && "Loading..."}
          {error && `Error uploading file: ${error}`}
        </p>
      </div>
      <div className="flex gap-2 p-2">
        {Object.values(images).map((o) => (
          <Card key={o.id}>
            <CardHeader>
              <CardTitle>{o.name}</CardTitle>
              <CardDescription>{o.uploadedAt.toLocaleString()}</CardDescription>
              <Button onClick={handleRemoveImage(o)}>Delete</Button>
            </CardHeader>
            <CardContent>
              <img src={`${API_URL}/static/${o.path}`} />
            </CardContent>
            <CardFooter>
              <p>
                {o.numCompressions} compression
                {o.numCompressions !== 1 ? "s" : ""}
              </p>
              <Button onClick={() => navigate(`/image/${o.id}`)}>
                View compressions
              </Button>
            </CardFooter>
          </Card>
        ))}
      </div>
      <Alert variant="destructive">
        <ExclamationTriangleIcon className="h-4 w-4" />
        <AlertTitle>Error</AlertTitle>
        <AlertDescription>
          Your session has expired. Please log in again.
        </AlertDescription>
      </Alert>
    </>
  );
}

export default App;
