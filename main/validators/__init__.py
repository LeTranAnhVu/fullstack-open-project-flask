class Validator():
    def __init__(self, name):
        self.errors = []
        self.name = name

    def _required(self, value):
        if not value:
            self.errors.append(f'{self.name} is required')
        return self

    def _maxlen(self, value, max):
        if len(value) > max:
            self.errors.append(f'{self.name} is maximum {max} characters')
        return self

    def _minlen(self, value, min):
        if len(value) < min:
            self.errors.append(f'{self.name} is minimum {min} characters')
        return self

    def _unique(self, col_value, model):
        if model.query.filter(getattr(model, self.name) == col_value).first():
            self.errors.append(f'{self.name} is existed')
        return self

    def _special_character_validator(self, value):
        _str = '.,!@#$% '
        display_str = '.,!@#$%<space>'
        for c in _str:
            if c in value:
                self.errors.append(f'{self.name} do not allow {display_str}')
                break
        return self

    def _confirm_password_validator(self, pw, c_pw):
        if (not pw) or (not c_pw) or (pw != c_pw):
            self.errors.append('password and confirm_password are not matched')
        return self
