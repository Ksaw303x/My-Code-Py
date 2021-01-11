import matplotlib.pyplot as plt
from pvlv_database import Database


class LevelUpGraphBuilder(object):

    @staticmethod
    def __format_data(guild_id, user_id):
        db = Database(guild_id, user_id)
        data = db.user.guild.msg.msg_log.log_by_day

        plot_data = [0]

        for idx, el in enumerate(data):
            value = el[1] + plot_data[idx]
            plot_data.append(value)

        plot_data.pop(0)
        print(plot_data)

        """
        for idx, value in enumerate(plot_data):
            text_len = value * 30 / 11
            xp = text_len * 12 / 30
            plot_data[idx] = xp
        """

        return plot_data

    def plot(self, ):

        u = [
            ('-1001444141366', 153519583),
            ('-1001444141366', 36974410),
            ('-1001444141366', 338674622),
            ('-1001444141366', 141619470),
            ('-1001444141366', 459725844),
            ('-1001444141366', 139393921),
        ]

        plot_data = []
        for guild_id, user_id in u:
            plot_data.append(self.__format_data(guild_id, user_id))

        fig, ax = plt.subplots()

        ax.plot(plot_data[0], '.-', color='#aa0504', alpha=0.7, label='Mattia')
        ax.plot(plot_data[1], '.-', color='#110000', alpha=0.7, label='Alberto')
        ax.plot(plot_data[2], '.-', color='#087800', alpha=0.7, label='Simone')
        # ax.plot(plot_data[3], '.-', color='#8df8fc', alpha=0.7, label='Luca')
        # ax.plot(plot_data[4], '.-', color='#2005b8', alpha=0.7, label='Andrea')
        # ax.plot(plot_data[5], '.-', color='#b88b05', alpha=0.7, label='Jacopo')

        plt.grid(axis='y', alpha=0.75)

        legend = ax.legend(loc='upper center', shadow=True, fontsize='x-large')
        legend.get_frame()

        plt.title('Messages sent by month')
        plt.ylabel('Xp')
        # plt.xlabel('First date: {} - Last Date: {}'.format(first_date, last_date))
        plt.savefig('plots_out/g.png')
        plt.show()


if __name__ == '__main__':
    i = LevelUpGraphBuilder()
    i.plot()
