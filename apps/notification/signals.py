from django.dispatch import Signal

notify = Signal(providing_args=[

				'receiver',
				'actor',
				'verb',
				'timestamp',
				'level'

	])