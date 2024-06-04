import cv2
import os


def extract_frames(video_path, output_folder, frame_rate=1):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cap = cv2.VideoCapture(video_path)
    count = 0
    success, image = cap.read()

    while success:
        if int(cap.get(cv2.CAP_PROP_POS_FRAMES)) % frame_rate == 0:
            cv2.imwrite(os.path.join(output_folder, f'frame{count}.jpg'), image)
            count += 1
        success, image = cap.read()

    cap.release()


# Klasör içindeki videoları işleme
dataset_dir = 'dataset'
for exercise_folder in os.listdir(dataset_dir):
    exercise_path = os.path.join(dataset_dir, exercise_folder)
    if os.path.isdir(exercise_path):
        for video_file in os.listdir(exercise_path):
            if video_file.endswith('.mp4'):  # Video dosya formatı
                video_path = os.path.join(exercise_path, video_file)
                output_folder = os.path.join(exercise_path, 'frames', video_file.split('.')[0])
                extract_frames(video_path, output_folder)
