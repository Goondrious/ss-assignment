import { useState, useEffect, useRef, useContext } from "react";
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
import {
  addCompressionToAPI,
  authenticatedFetch,
  deleteImageCompressionFromAPI,
  fetchImageCompressionsFromAPI,
  fetchImageFromAPI,
} from "@/lib/api";
import { API_URL, TOKEN_STORAGE_KEY } from "@/lib/constants";
import { AppContext } from "@/hooks/context";
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert";
import { ExclamationTriangleIcon } from "@radix-ui/react-icons";
import { TrashIcon } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

const EMPTY_COMPRESSION_FORM = {
  quality: 60,
  resizeWidth: 0,
};

export default () => {
  const { imageId } = useParams();
  const { setLoading, setToast } = useContext(AppContext);

  const [image, setImage] = useState<UserImage | undefined>();
  useEffect(() => {
    const fetchImage = async (imageId: string) => {
      const token = localStorage.getItem(TOKEN_STORAGE_KEY);
      if (!token) return;

      setLoading(true);
      const { data, error } = await fetchImageFromAPI(imageId, token);
      setLoading(false);

      if (error) {
        setToast({ type: "error", message: error });
        return;
      }

      setImage(data);
    };

    if (imageId) fetchImage(imageId);
  }, [imageId]);

  const {
    imageCompressions,
    setImageCompressions,
    addImageCompression,
    removeImageCompression,
  } = useImageCompressions();

  useEffect(() => {
    const fetchImageCompressions = async (imageId: string) => {
      const token = localStorage.getItem(TOKEN_STORAGE_KEY);
      if (!token) return;

      setLoading(true);
      const { data, error } = await fetchImageCompressionsFromAPI(
        imageId,
        token
      );
      setLoading(false);

      if (error) {
        setToast({ type: "error", message: error });
        return;
      }

      setImageCompressions(data);
    };

    if (imageId) fetchImageCompressions(imageId);
  }, [imageId]);

  const [form, setForm] = useState(EMPTY_COMPRESSION_FORM);
  const handleFormChange =
    (key: string) => (e: React.ChangeEvent<HTMLInputElement>) => {
      setForm((o) => ({ ...o, [key]: e.target.value }));
    };

  const handleAddImageCompression = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!imageId || form.quality === undefined) return;

    const token = localStorage.getItem(TOKEN_STORAGE_KEY);
    if (!token) return;

    setLoading(true);
    const { data, error } = await addCompressionToAPI(
      { imageId, ...form },
      token
    );
    setLoading(false);

    if (error) {
      setToast({ type: "error", message: error });
      return;
    }

    setToast({ type: "success", message: "New image compression added!" });
    addImageCompression(data.compression);
  };

  const handleRemoveImageCompression =
    (compression: ImageCompression) => async () => {
      const token = localStorage.getItem(TOKEN_STORAGE_KEY);
      if (!token) return;

      setLoading(true);
      const { error } = await deleteImageCompressionFromAPI(
        compression.image_id,
        compression.id,
        token
      );
      setLoading(false);

      if (error) {
        setToast({ type: "error", message: error });
        return;
      }

      setToast({ type: "success", message: "Image compression deleted" });
      removeImageCompression(compression);
    };

  const [imageWidth, setImageWidth] = useState<number | undefined>();

  return (
    <div className="w-full flex flex-col justify-center items-center mt-2">
      {image && (
        <Card>
          <CardHeader>
            <CardTitle>
              {image.name} - {image.size} bytes
            </CardTitle>
            <CardDescription>
              Uploaded at {image.uploaded_at.toLocaleString()}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <img
              src={`${API_URL}${image.signed_url}`}
              onLoad={(e) => {
                // unsure why this onLoad event isn't picking up .naturalWidth property
                // @ts-expect-error
                const width = e.target.naturalWidth;
                setImageWidth(width);
                setForm((o) => ({ ...o, resizeWidth: width }));
              }}
            />
          </CardContent>
          <CardFooter>
            {Object.keys(imageCompressions).length < 10 ? (
              <form
                onSubmit={handleAddImageCompression}
                method="post"
                className="flex items-center flex-wrap gap-4 mt-2"
              >
                {image?.extension === "jpeg" ? (
                  <div className="flex gap-1 items-center">
                    <Label htmlFor="quality" className="font-semibold">
                      Quality
                    </Label>
                    <Input
                      name="quality"
                      onChange={handleFormChange("quality")}
                      value={form["quality"]}
                      type="number"
                      min={1}
                      max={100}
                    />
                  </div>
                ) : (
                  <Alert variant="default">
                    <ExclamationTriangleIcon className="h-4 w-4" />
                    <AlertTitle>Image compression settings </AlertTitle>
                    <AlertDescription>
                      PNG and GIF files can only be resized
                    </AlertDescription>
                  </Alert>
                )}
                {imageWidth && (
                  <div className="flex gap-1 items-center">
                    <Label htmlFor="resizeWidth" className="font-semibold">
                      Resize Width
                    </Label>
                    <Input
                      name="resizeWidth"
                      onChange={handleFormChange("resizeWidth")}
                      value={form["resizeWidth"]}
                      type="number"
                      min={0}
                      max={imageWidth}
                    />
                  </div>
                )}
                <Button type="submit">Add New Compression</Button>
              </form>
            ) : (
              <Alert variant="default">
                <ExclamationTriangleIcon className="h-4 w-4" />
                <AlertTitle>Compression Limit Reached</AlertTitle>
                <AlertDescription>
                  You can only have 10 compressions per image. Please delete
                  some.
                </AlertDescription>
              </Alert>
            )}
          </CardFooter>
        </Card>
      )}

      <div className="w-full mt-4">
        {Object.keys(imageCompressions).length > 0 ? (
          <h1 className="text-xl font-semibold">Your Compressions</h1>
        ) : (
          <Alert variant="default">
            <ExclamationTriangleIcon className="h-4 w-4" />
            <AlertTitle>Image Compressions</AlertTitle>
            <AlertDescription>
              You have no compressions. Use the settings above to create one!
            </AlertDescription>
          </Alert>
        )}
      </div>
      <div className="flex gap-2 p-2 flex-wrap">
        {Object.values(imageCompressions).map((o) => (
          <Card key={o.id}>
            <CardHeader>
              <div className="flex justify-between">
                <div className="flex flex-col gap-1">
                  <CardTitle>
                    {o.size} bytes
                    <br />
                    {o.resize_width}px wide
                    <br />
                    {image?.extension === "jpeg" ? `${o.quality} quality` : ""}
                  </CardTitle>
                  <CardDescription>
                    Created at {o.created_at.toLocaleString()}
                  </CardDescription>
                </div>
                <Button
                  variant="destructive"
                  onClick={handleRemoveImageCompression(o)}
                >
                  <TrashIcon />
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <img src={`${API_URL}${o.signed_url}`} />
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};
