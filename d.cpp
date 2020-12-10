void A();

void D()
{
    A();
}

void C();
void E();

void A()
{
    C();
    E();
}

void G();

void E()
{
    G();
    D();
}

void F();

void G()
{
    F();
}
