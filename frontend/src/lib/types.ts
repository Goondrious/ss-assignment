export type User = {
  username: string;
};

export type UserImage = {
  id: string;
  user_id: string;
  path: string;
  name: string;
  extension: string;
  size: number;
  uploaded_at: Date;
  num_compressions?: number;
  signed_url?: string;
};

export type ImageCompression = {
  image_id: string;
  id: string;
  path: string;
  quality: number;
  resize_width: number;
  size: number;
  created_at: Date;
  signed_url?: string;
};

export type Toast = {
  message: string;
  type: string;
};

export type NewCompressionInput = {
  imageId: string;
  quality: number;
  resizeWidth: number;
};
