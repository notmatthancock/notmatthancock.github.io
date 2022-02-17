---
layout: post
title: Dialect-dependent column types in sqlalchemy
area: notes
tags:
- software
- python
- databases
---

Recently I was working on a system that uses [postgres](https://www.postgresql.org/) as the database storage choice. The system uses [sqlalchemy core](https://docs.sqlalchemy.org/en/14/core/) for database interactions, so it is *almost* agnostic to the particular choice of database backend. It is not completely agnostic because it is using an [ARRAY column type](https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.ARRAY) in a few places, which is only supported by postgres.

I wanted to implement some light-weight testing against the database using sqlite instead of postgres. It turns out there are [tools for doing this in sqlalchemy](https://docs.sqlalchemy.org/en/14/core/custom_types.html), using TypeDecorators.

### SQLAlchemy's TypeDecorator

We can implement a custom type that swaps to JSON when the backend dialect is sqlite and uses postgres's native Array type otherwise. Note that you lose inner typing in the sqlite case, but it's better than nothing!

{% highlight python %}
from typing import Optional, Type

from sqlalchemy.types import ARRAY, JSON, TypeDecorator, TypeEngine


class MaybeArray(TypeDecorator):
    """Column type that uses native ARRAY type for psql and JSON for sqlite

    Provide the inner type for the ARRAY during initialization. If the backend
    is sqlite, then the inner type is ignored.

    Raises ValueError if the dialect is neither "postgresql" nor "sqlite" or
    if no inner type is provided and the backend is postgresql.
    """

    # This is required at initialization by the TypeDecorator class, but
    # the actual impl choice is selected by `load_dialect_impl`.
    impl = JSON

    def __init__(
        self,
        inner_type: Optional[Type[TypeEngine]] = None,
        *args, **kwargs
    ):
        self.inner_type = inner_type
        super().__init__(*args, **kwargs)

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            if self.inner_type is None:
                raise ValueError("inner type may not be None for postgres")
            return dialect.type_descriptor(ARRAY(self.inner_type))
        elif dialect.name == "sqlite":
            return dialect.type_descriptor(JSON)
        else:
            raise ValueError(f'dialect "{dialect.name}" not supported')
{% endhighlight %}

### Usage in Table definitions

You would use the `MaybeArray` type decorator just as you would any other column type in your code.

For example, your table definition would change from..

{% highlight python %}
SHOPPING_TABLE = Table(
    "shopping_list",
    METADATA,
    Column("id", Integer(), primary_key=True),
    Column("names", ARRAY(String)),
    Column("prices", ARRAY(Float)),
)
{% endhighlight %}

to...

{% highlight python %}
SHOPPING_TABLE = Table(
    "shopping_list",
    METADATA,
    Column("id", Integer(), primary_key=True),
    Column("names", MaybeArray(String)),
    Column("prices", MaybeArray(Float)),
)
{% endhighlight %}

### Conclusions

This turned out to work perfectly! However, in this particular system, there was another dialect-dependency hidden beneath the surface that prevented sqlite usage: there are many SQL `RETURNING` statements used throughout the code. I was happy to see this [already on the SQLAchemy developers' radars](https://github.com/sqlalchemy/sqlalchemy/issues/6195). For now, we'll continue testing against postgres, which is probably a better move in the long run anyhow :)
