import asyncio

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, User, Profile, Post, Order, Product


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    print("user", user)
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    # result: Result = await session.execute(stmt)
    # # user: User | None = result.scalar_one_or_none()
    # user: User | None = result.scalar_one()
    user: User | None = await session.scalar(stmt)
    print("found user", username, user)
    return user


async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
) -> Profile:
    profile = Profile(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
    )
    session.add(profile)
    await session.commit()
    return profile


async def show_users_with_profiles(session: AsyncSession):
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
    # result: Result = await session.execute(stmt)
    # users = result.scalars()
    users = await session.scalars(stmt)
    for user in users:
        print(user)
        print(user.profile.first_name)


async def create_posts(
    session: AsyncSession,
    user_id: int,
    *posts_titles: str,
) -> list[Post]:
    posts = [Post(title=title, user_id=user_id) for title in posts_titles]
    session.add_all(posts)
    await session.commit()
    print(posts)
    return posts


async def get_users_with_posts(
    session: AsyncSession,
):
    # stmt = select(User).options(joinedload(User.posts)).order_by(User.id)
    stmt = (
        select(User)
        .options(
            # joinedload(User.posts),
            selectinload(User.posts),
        )
        .order_by(User.id)
    )
    # users = await session.scalars(stmt)
    # result: Result = await session.execute(stmt)
    # # users = result.unique().scalars()
    # users = result.scalars()
    users = await session.scalars(stmt)

    # for user in users.unique():  # type: User
    for user in users:  # type: User
        print("**" * 10)
        print(user)
        for post in user.posts:
            print("-", post)


async def get_users_with_posts_and_profiles(
    session: AsyncSession,
):
    stmt = (
        select(User)
        .options(
            joinedload(User.profile),
            selectinload(User.posts),
        )
        .order_by(User.id)
    )
    users = await session.scalars(stmt)

    for user in users:  # type: User
        print("**" * 10)
        print(user, user.profile and user.profile.first_name)
        for post in user.posts:
            print("-", post)


async def get_posts_with_authors(session: AsyncSession):
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)

    for post in posts:  # type: Post
        print("post", post)
        print("author", post.user)


async def get_profiles_with_users_and_users_with_posts(session: AsyncSession):
    stmt = (
        select(Profile)
        .join(Profile.user)
        .options(
            joinedload(Profile.user).selectinload(User.posts),
        )
        .where(User.username == "john")
        .order_by(Profile.id)
    )

    profiles = await session.scalars(stmt)

    for profile in profiles:
        print(profile.first_name, profile.user)
        print(profile.user.posts)


async def create_order(session: AsyncSession, promocode: str | None = None) -> Order:
    order = Order(promocode=promocode)
    session.add(order)
    await session.commit()
    return order


async def create_product(
    session: AsyncSession, name: str, descriprion: str, price: int
) -> Product:
    product = Product(name=name, description=descriprion, price=price)
    session.add(product)
    await session.commit()

    return product

async def create_orders_and_products(session: AsyncSession):
    order1 = await create_order(session, promocode="123")
    order2 = await create_order(session, promocode="FastAPI intro")
    mouse = await create_product(
        session=session, name="Mouse", descriprion="Mouse", price=100
    )
    keyboard = await create_product(
        session=session, name="Keyboard", descriprion="Keyboard", price=200
    )
    display = await create_product(
        session=session, name="Display", descriprion="Display", price=500
    )

    order1 = await session.scalar(
        select(Order)
        .where(Order.id == order1.id)
        .options(
            selectinload(Order.products),
        ),
    )
    order2 = await session.scalar(
        select(Order)
        .where(Order.id == order2.id)
        .options(
            selectinload(Order.products),
        ),
    )

    order1.products.append(mouse)
    order1.products.append(keyboard)
    # order2.products.append(keyboard)
    # order2.products.append(display)

    order2.products = [keyboard, display]

    await session.commit()


async def get_order_with_products(session: AsyncSession) -> list[Order]:
    stmt = select(Order).options(selectinload(Order.products)).order_by(Order.id)
    orders = await session.scalars(stmt)
    return list(orders)


async def main_relations(session: AsyncSession):
    await create_user(session=session, username="john")
    await create_user(session=session, username="alice")
    await create_user(session=session, username="sam")
    user_sam = await get_user_by_username(session=session, username="sam")
    user_john = await get_user_by_username(session=session, username="john")
    # user_bob = await get_user_by_username(session=session, username="bob")
    await create_user_profile(
        session=session,
        user_id=user_john.id,
        first_name="John",
    )
    await create_user_profile(
        session=session,
        user_id=user_sam.id,
        first_name="Sam",
        last_name="White",
    )
    await show_users_with_profiles(session=session)
    await create_posts(
        session,
        user_john.id,
        "SQLA 2.0",
        "SQLA Joins",
    )
    await create_posts(
        session,
        user_sam.id,
        "FastAPI intro",
        "FastAPI Advanced",
        "FastAPI more",
    )
    await get_users_with_posts(session=session)
    await get_posts_with_authors(session=session)
    await get_users_with_posts_and_profiles(session=session)
    await get_profiles_with_users_and_users_with_posts(session=session)


async def demo_m2m(session: AsyncSession):
    orders = await get_order_with_products(session=session)
    for order in orders:
        print(order.id, order.promocode, order.created_at, "products:")
        for product in order.products:
            print("-", product.id, product.name, product.price)

async def main():
    async with db_helper.session_factory() as session:
        # await main_relations(session=session)
        await demo_m2m(session=session)


if __name__ == "__main__":
    asyncio.run(main())
