import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from gui import SelectDefinitionSourceView, SelectItemView, DownloadProgressView, FinishedView
import PakDownloader
import logging
from typing import Any

logging.basicConfig(level=logging.INFO)

# ウィンドウオブジェクトを作成
window = tk.Tk()

# ウィンドウのタイトルを設定
window.title("Simutrans Pak Manager")

# ウィンドウのサイズと位置を設定
window.geometry("400x300+100+100")

# ウィンドウが閉じられたときの処理
def on_closing():
    # 確認ダイアログを表示
    if messagebox.askokcancel("終了", "本当に終了しますか？"):
        # ウィンドウを閉じる
        window.destroy()

# ウィンドウが閉じられたときにon_closing関数を呼び出すように設定
window.protocol("WM_DELETE_WINDOW", on_closing)

def showSelectItemView(definition_json):
    view = SelectItemView.SelectItemView(window, definition_json, start_download_and_show_progress_view)
    view.frame.pack()

def start_download_and_show_progress_view(
        definition_json: Any, 
        selected_index: int, 
        destination_path: str
    ) -> None:
    progress_view = DownloadProgressView.DownloadProgressView(window)
    progress_view.frame.pack()
    PakDownloader.download_from_definition(
        directory=destination_path, 
        definition_json=definition_json, 
        index=selected_index, 
        show_message=progress_view.add_message, 
        report_progress_percent=progress_view.update_progress
    )
    progress_view.frame.pack_forget()
    finished_view = FinishedView.FinishedView(window)
    finished_view.frame.pack()

# 各ページのフレームオブジェクトを作成
view1 = SelectDefinitionSourceView.SelectDefinitionSourceView(window, show_select_item_view=showSelectItemView)

# 1ページ目のフレームを表示する（最初は1ページ目から始めるため）
view1.frame.pack()

# ウィンドウのメインループを開始
window.mainloop()
