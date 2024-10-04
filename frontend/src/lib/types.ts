export type UserImage = {
  id: string;
  userId: string;
  path: string;
  name: string;
  uploadedAt: Date;
  numCompressions: number;
};

export type ImageCompression = {
  imageId: string;
  id: string;
  path: string;
  quality: number;
  size: number;
  createdAt: Date;
};
