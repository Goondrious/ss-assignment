export type User = {
  username: string;
};

export type UserImage = {
  id: string;
  user_id: string;
  path: string;
  name: string;
  uploaded_at: Date;
  num_compressions: number;
};

export type ImageCompression = {
  image_id: string;
  id: string;
  path: string;
  quality: number;
  size: number;
  created_at: Date;
};
