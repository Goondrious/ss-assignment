import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from "@/components/ui/card";
import { ImageCompression, UserImage } from "@/lib/types";
import { useImageCompressions } from "@/hooks/image";

const API_URL = "http://localhost:8000";

const IMAGE = {
  id: `${Math.random()}`,
  userId: "1",
  path: "/elephant test-compressed.jpg",
  name: "Elephant",
  uploadedAt: new Date(),
  numCompressions: 2,
};

const NEW_COMPRESSION = {
  id: `${Math.random()}`,
  imageId: "1",
  path: "/elephant test-compressed.jpg",
  createdAt: new Date(),
  size: 100,
  quality: 100,
};

const IMAGE_COMPRESSIONS: ImageCompression[] = [
  {
    id: "1",
    imageId: "1",
    path: "/elephant test-compressed.jpg",
    createdAt: new Date(),
    size: 100,
    quality: 100,
  },
  {
    id: "2",
    imageId: "1",
    path: "/link-compressed.png",
    createdAt: new Date(),
    size: 50,
    quality: 80,
  },
];

export default () => {
  const { imageId } = useParams();
  const navigate = useNavigate();

  const [image, setImage] = useState<UserImage | undefined>();
  useEffect(() => {
    setImage(IMAGE);
  }, []);

  const {
    imageCompressions,
    setImageCompressions,
    addImageCompression,
    removeImageCompression,
  } = useImageCompressions();

  useEffect(() => {
    setImageCompressions(
      IMAGE_COMPRESSIONS.reduce((agg, o) => ({ ...agg, [o.id]: o }), {})
    );
  }, []);

  const handleAddImage = () => {
    addImageCompression(NEW_COMPRESSION);
  };

  const handleRemoveImageCompression =
    (compression: ImageCompression) => () => {
      removeImageCompression(compression);
    };

  return (
    <div>
      Hello from {imageId} page.
      <Button onClick={() => navigate("/")}>Home</Button>
      {image && (
        <>
          <div className="text-lg">{image.name}</div>
          <div className="text-md">{image.uploadedAt.toLocaleString()}</div>
        </>
      )}
      <Button onClick={handleAddImage}>Add New Compression</Button>
      <div className="flex gap-2 p-2">
        {Object.values(imageCompressions).map((o) => (
          <Card key={o.id}>
            <CardHeader>
              <CardTitle>
                {o.size} - {o.quality}
              </CardTitle>
              <CardDescription>{o.createdAt.toLocaleString()}</CardDescription>
            </CardHeader>
            <CardContent>
              <img src={`${API_URL}/static/${o.path}`} />
            </CardContent>
            <CardFooter>
              <Button onClick={handleRemoveImageCompression(o)}>Delete</Button>
            </CardFooter>
          </Card>
        ))}
      </div>
    </div>
  );
};
