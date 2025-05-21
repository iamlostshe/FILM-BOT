from film_bot.models import Anime, Dorama


class FilmBot:
    """Film bot class."""

    def add_serial(self, message):
        """Adding a dorama or anime to the database

        :param message: dorama or anime
        :return:
        """
        chat_id = message.chat.id
        serial = message.text
        msg = self.bot.reply_to(message, "Введите название сериала, который вы хотите добавить")
        self.bot.register_next_step_handler(msg, self.process_name_serial, chat_id, serial)

    def process_name_serial(self, message, chat_id, serial):
        name = message.text
        if (serial == "дорама") or (serial == "дорамы"):
            self.user_data[chat_id]["current_dorama_name"] = name
        else:
            self.user_data[chat_id]["current_anime_name"] = name
        msg = self.bot.reply_to(message, "Введите комментарии к сериалу")
        self.bot.register_next_step_handler(msg, self.process_comment_serial, chat_id, serial)

    def process_comment_serial(self, message, chat_id, serial):
        comment = message.text
        if (serial == "дорама") or (serial == "дорамы"):
            name = self.user_data[chat_id].pop("current_dorama_name")
            self.user_data[chat_id]["doramas"].append(Dorama(name, comment))
            self.save_serial(chat_id, name, comment, serial)
        else:
            name = self.user_data[chat_id].pop("current_anime_name")
            self.user_data[chat_id]["anime"].append(Anime(name, comment))
            self.save_serial(chat_id, name, comment, serial)
        self.bot.send_message(chat_id, f"В раздел {serial} добавлен '{name}' с комментарием: {comment}")

    def save_serial(self, chat_id, name, comment, serial):
        cursor = self.conn.cursor()
        if (serial == "дорама") or (serial == "дорамы"):
            cursor.execute("INSERT INTO doramas (chat_id, name, comment) VALUES (?, ?, ?)",
                           (chat_id, name, comment))
        else:
            cursor.execute("INSERT INTO anime (chat_id, name, comment) VALUES (?, ?, ?)",
                           (chat_id, name, comment))
        self.conn.commit()

    def delete_serial(self, message):
        """Deleting a dorama or anime from the database

        :param message: dorama or anime
        :return:
        """
        chat_id = message.chat.id
        serial = message.text
        msg = self.bot.reply_to(message, "Введите название сериала, который нужно удалить:")
        self.bot.register_next_step_handler(msg, self.process_delete_serial, chat_id, serial)

    def process_delete_serial(self, message, chat_id, serial):
        name = message.text
        self.user_data[chat_id]["doramas"] = [dorama for dorama in self.user_data[chat_id]["doramas"] if dorama.name != name]
        self.delete_serial_from_db(chat_id, name, serial)
        self.bot.send_message(chat_id, f"{serial} {name} удалёна")

    def delete_serial_from_db(self, chat_id, name, serial):
        cursor = self.conn.cursor()
        if (serial == "дорама") or (serial == "дорамы"):
            cursor.execute("DELETE FROM doramas WHERE chat_id = ? AND name = ?", (chat_id, name))
        else:
            cursor.execute("DELETE FROM anime WHERE chat_id = ? AND name = ?", (chat_id, name))
        self.conn.commit()

    def list_serial(self, message):
        """Displaying a list of favorites

        :param message:
        :return:
        """
        chat_id = message.chat.id
        serial = message.text
        valid_serials = []
        if (serial == "дорама") or (serial == "дорамы"):
            doramas = self.user_data[chat_id]["doramas"]
            self.user_data[chat_id]["doramas"] = valid_serials
            if not doramas:
                self.bot.send_message(chat_id, "Ваш список пуст 🥺")
            else:
                doramas_str = "\n".join(str(dorama) for dorama in doramas)
                self.bot.send_message(chat_id, f"Ваш список избранного 🔥:\n{doramas_str}")
        else:
            anime = self.user_data[chat_id]["anime"]
            self.user_data[chat_id]["doramas"] = valid_serials
            if not anime:
                self.bot.send_message(chat_id, "Ваш список пуст 🥺")
            else:
                anime_str = "\n".join(str(anima) for anima in anime)
                self.bot.send_message(chat_id, f"Ваш список избранного 🔥:\n{anime_str}")
