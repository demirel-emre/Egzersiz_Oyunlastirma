import cv2
import numpy as np
import mediapipe as mp
from keras.models import load_model
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import time

# MediaPipe kurulum ve yapılandırma
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Eğitilmiş modeli yükleme
model = load_model('fitness_model.h5')

# Egzersiz sınıfları
classes = ['chest_squeezes', 'high_knees', 'leg_curls', 'punches', 'squat']


class FitnessApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("Emre Demirel | Egzersiz Model")
        self.geometry("800x600")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=BOTH, expand=True)

        self.prediction_page = PredictionPage(self.notebook)
        self.exercise_page = ExercisePage(self.notebook)

        self.notebook.add(self.prediction_page, text="Yapılan Hareketi Tahmin Et")
        self.notebook.add(self.exercise_page, text="Hareketler Arasından Seçim Yap")


class PredictionPage(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.video_button = Button(self, text="Video Seç", command=self.select_video)
        self.video_button.pack(pady=10)

        self.camera_button = Button(self, text="Kamera Aç", command=self.select_camera)
        self.camera_button.pack(pady=10)

        self.predictions_label = Label(self, text="Tahminler:")
        self.predictions_label.pack(pady=10)

    def select_video(self):
        video_path = filedialog.askopenfilename(title="Video Seçimi", filetypes=[("Video dosyaları", "*.mp4;*.avi")])
        if video_path:
            self.perform_prediction(video_path)

    def select_camera(self):
        self.perform_prediction(0)

    def perform_prediction(self, video_path):
        if video_path != 0:
            cap = cv2.VideoCapture(video_path)
        else:
            cap = cv2.VideoCapture(0)

        start_time = time.time()
        prediction_list = []
        while time.time() - start_time < 10:
            ret, frame = cap.read()
            if not ret:
                break

            # MediaPipe ile vücut hareketlerini tanıma
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                landmark_array = np.array([[landmark.x, landmark.y, landmark.z] for landmark in landmarks]).flatten()

               

                resized_frame = cv2.resize(frame, (150, 150))
                normalized_frame = resized_frame / 255.0
                input_frame = np.expand_dims(normalized_frame, axis=0)
                predictions = model.predict(input_frame)
                predicted_class_index = np.argmax(predictions)
                predicted_class = classes[predicted_class_index]
                prediction_list.append(predicted_class)

            cv2.imshow("Video", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        if len(prediction_list) > 0:
            prediction_count = len(prediction_list)
            prediction_counts = {prediction: prediction_list.count(prediction) for prediction in set(prediction_list)}
            prediction_text = "\n".join(
                f"{prediction}: %{(count / prediction_count) * 100:.2f}" for prediction, count in
                prediction_counts.items())
            self.predictions_label.config(text="Tahminler:\n" + prediction_text)
        else:
            self.predictions_label.config(text="Herhangi bir tahmin yapılmadı.")


class ExercisePage(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.selected_exercise_label = Label(self, text="")
        self.selected_exercise_label.pack(pady=10)

        self.correct_count_label = Label(self, text="")
        self.correct_count_label.pack(pady=10)

        self.total_count_label = Label(self, text="")
        self.total_count_label.pack(pady=10)

        self.score_label = Label(self, text="")
        self.score_label.pack(pady=10)

        self.exercise_var = StringVar()
        self.exercise_menu = OptionMenu(self, self.exercise_var, *classes)
        self.exercise_menu.pack(pady=10)

        self.select_button = Button(self, text="Hareket Seç", command=self.select_exercise)
        self.select_button.pack(pady=10)

        self.video_button = None
        self.camera_button = None

    def select_exercise(self):
        selected_exercise = self.exercise_var.get()
        correct_count = 0
        total_count = 0

        self.selected_exercise_label.config(text="Seçilen Hareket: " + selected_exercise)
        self.correct_count_label.config(text="Doğru Tahmin Sayısı: " + str(correct_count))
        self.total_count_label.config(text="Toplam Hareket Sayısı: " + str(total_count))
        self.score_label.config(text="Skor: 0")

        if self.video_button:
            self.video_button.pack_forget()
            self.video_button = None
        if self.camera_button:
            self.camera_button.pack_forget()
            self.camera_button = None

        self.video_button = Button(self, text="Video Seç", command=lambda: self.select_video(selected_exercise))
        self.video_button.pack(pady=10)

        self.camera_button = Button(self, text="Kamera Aç", command=lambda: self.select_camera(selected_exercise))
        self.camera_button.pack(pady=10)

    def select_video(self, selected_exercise):
        video_path = filedialog.askopenfilename(title="Video Seçimi", filetypes=[("Video dosyaları", "*.mp4;*.avi")])
        if video_path:
            cap = cv2.VideoCapture(video_path)
            correct_count = 0
            total_count = 0
            score = 0

            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                resized_frame = cv2.resize(frame, (150, 150))
                normalized_frame = resized_frame / 255.0
                input_frame = np.expand_dims(normalized_frame, axis=0)
                predictions = model.predict(input_frame)
                predicted_class_index = np.argmax(predictions)
                predicted_class = classes[predicted_class_index]
                total_count += 1
                if predicted_class == selected_exercise:
                    correct_count += 1
                    score += 10
                    cv2.putText(frame, "Doğru Yapiyorsunuz", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    cv2.putText(frame, "Yanlis Yapiyorsunuz", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                cv2.imshow("Video", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()

            self.correct_count_label.config(text="Doğru Tahmin Sayısı: " + str(correct_count))
            self.total_count_label.config(text="Toplam Hareket Sayısı: " + str(total_count))
            self.score_label.config(text="Skor: " + str(score))

    def select_camera(self, selected_exercise):
        cap = cv2.VideoCapture(0)
        correct_count = 0
        total_count = 0
        score = 0

        # Örnek bir iskelet göstermek için MediaPipe kullanımı
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # MediaPipe ile vücut hareketlerini tanıma
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            # Eğer vücut algılanırsa
            if results.pose_landmarks:
                # Vücut iskeletini çizme
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2,
                                                                                 circle_radius=2),
                    connection_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2))

            resized_frame = cv2.resize(frame, (150, 150))
            normalized_frame = resized_frame / 255.0
            input_frame = np.expand_dims(normalized_frame, axis=0)
            predictions = model.predict(input_frame)
            predicted_class_index = np.argmax(predictions)
            predicted_class = classes[predicted_class_index]
            total_count += 1
            if predicted_class == selected_exercise:
                correct_count += 1
                score += 10
                cv2.putText(frame, "Dogru Yapiyorsunuz", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Yanlis Yapiyorsunuz", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.imshow("Kamera", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        self.correct_count_label.config(text="Doğru Tahmin Sayısı: " + str(correct_count))
        self.total_count_label.config(text="Toplam Hareket Sayısı: " + str(total_count))
        self.score_label.config(text="Skor: " + str(score))


app = FitnessApp()
app.mainloop()
