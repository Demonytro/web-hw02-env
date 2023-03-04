def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'No contact with this name, try again'
        except ValueError as exception:
            return exception.args[0]
        except IndexError:
            return 'Seems, some mistake. Please, try again'
        except TypeError as exception:
            return "Sorry, I didn't understand this command, please try again"
        except AttributeError as exception:
            return "Sorry, no such attribute("
        except FileExistsError:
            return 'note with this name  already exists'
        except FileNotFoundError:
            return 'there is no note with this name'

    return inner
