import { useState } from "react";
import { ImageCompression, UserImage } from "@/lib/types";

export const useImages = () => {
  const [images, setImages] = useState<{ [k: string]: UserImage }>({});

  const addImage = (image: UserImage) => {
    setImages((o) => ({ ...o, [image.id]: image }));
  };

  const removeImage = (image: UserImage) => {
    setImages((o) => {
      const update = { ...o };
      delete update[image.id];
      return update;
    });
  };

  return { images, setImages, addImage, removeImage };
};

export const useImageCompressions = () => {
  const [imageCompressions, setImageCompressions] = useState<{
    [k: string]: ImageCompression;
  }>({});

  const addImageCompression = (compression: ImageCompression) => {
    setImageCompressions((o) => ({ ...o, [compression.id]: compression }));
  };

  const removeImageCompression = (compression: ImageCompression) => {
    setImageCompressions((o) => {
      const update = { ...o };
      delete update[compression.id];
      return update;
    });
  };

  return {
    imageCompressions,
    setImageCompressions,
    addImageCompression,
    removeImageCompression,
  };
};
