from io import StringIO


class FieldSerializer:
    @staticmethod
    def serialize(field) -> StringIO:
        builder = StringIO()
        for x, y in field:
            builder.write(str(x) + ' ' + str(y) + '\n')
        return builder

    @staticmethod
    def deserialize(file) -> set:
        field = set()
        for line in file.readlines():
            x, y = (int(s) for s in line.split())
            field.add((x, y))
        return field
